import json
import os
from pathlib import Path

import chromadb
from dotenv import load_dotenv
from groq import Groq
from rank_bm25 import BM25Okapi
from sentence_transformers import SentenceTransformer

load_dotenv()

CHROMA_PATH = Path(__file__).parent / "chroma_db"
CHUNKS_PATH = Path(__file__).parent / "chunks.json"
COLLECTION_NAME = "uci_cs_guide"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
GROQ_MODEL = "llama-3.3-70b-versatile"
TOP_K = 5
RRF_K = 60  # constant in Reciprocal Rank Fusion formula

REFUSAL_PHRASE = "I don't have enough information on that based on the available documents."

SYSTEM_PROMPT = f"""You are a helpful assistant for UCI Computer Science students planning their courses.

Answer questions ONLY using the information in the context documents provided below.
Do NOT use any outside knowledge, training data, or general information — even if you are confident about the answer.
If the context documents do not contain enough information to answer the question, respond with exactly:
"{REFUSAL_PHRASE}"

Do not make assumptions or inferences beyond what is explicitly stated in the documents.
Be specific: quote or paraphrase the relevant parts of the documents in your answer.
Always include citations. When citing information, refer to the source by its filename as it appears in the document header (e.g. "According to rate_my_professor.txt..." or "A student on low_stress_cs_electives.txt noted...").

When the user uses pronouns or follow-up references ("which one", "those", "it", "that one", "of those") that refer to items from earlier in the conversation, limit your answer strictly to the courses, professors, or topics already mentioned in the prior conversation. Do not introduce new items from the context documents that were not part of the previous response."""

# Module-level singletons — loaded once, reused across all queries
_model: SentenceTransformer | None = None
_collection: chromadb.Collection | None = None
_client: Groq | None = None
_bm25: BM25Okapi | None = None
_bm25_chunks: list[dict] | None = None


def _load_resources() -> tuple[SentenceTransformer, chromadb.Collection, Groq]:
    global _model, _collection, _client
    if _model is None:
        _model = SentenceTransformer(EMBEDDING_MODEL)
    if _collection is None:
        db = chromadb.PersistentClient(path=str(CHROMA_PATH))
        _collection = db.get_collection(COLLECTION_NAME)
    if _client is None:
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("GROQ_API_KEY not set — copy .env.example to .env and add your key.")
        _client = Groq(api_key=api_key)
    return _model, _collection, _client


def _load_bm25() -> tuple[BM25Okapi, list[dict]]:
    global _bm25, _bm25_chunks
    if _bm25 is None:
        if not CHUNKS_PATH.exists():
            raise FileNotFoundError(
                f"{CHUNKS_PATH} not found — run embed.py to rebuild the index."
            )
        _bm25_chunks = json.loads(CHUNKS_PATH.read_text(encoding="utf-8"))
        tokenized = [c["text"].lower().split() for c in _bm25_chunks]
        _bm25 = BM25Okapi(tokenized)
    return _bm25, _bm25_chunks


def _retrieve_semantic(
    query: str,
    model: SentenceTransformer,
    collection: chromadb.Collection,
    k: int,
    source_filter: list[str] | None = None,
) -> list[dict]:
    embedding = model.encode([query])[0]
    query_kwargs: dict = dict(
        query_embeddings=[embedding.tolist()],
        n_results=k,
        include=["documents", "metadatas", "distances"],
    )
    if source_filter:
        query_kwargs["where"] = {"source": {"$in": source_filter}}
    results = collection.query(**query_kwargs)
    return [
        {
            "text": doc,
            "source": meta["source"],
            "chunk_index": meta["chunk_index"],
            "distance": round(dist, 4),
        }
        for doc, meta, dist in zip(
            results["documents"][0],
            results["metadatas"][0],
            results["distances"][0],
        )
    ]


def _retrieve_bm25(
    query: str, k: int, source_filter: list[str] | None = None
) -> list[dict]:
    bm25, chunks = _load_bm25()
    scores = bm25.get_scores(query.lower().split())
    eligible = (
        [i for i, c in enumerate(chunks) if c["source"] in source_filter]
        if source_filter
        else list(range(len(chunks)))
    )
    top_indices = sorted(eligible, key=lambda i: scores[i], reverse=True)[:k]
    return [
        {
            "text": chunks[i]["text"],
            "source": chunks[i]["source"],
            "chunk_index": i,
            "bm25_score": round(float(scores[i]), 4),
        }
        for i in top_indices
    ]


def _rrf_merge(semantic_chunks: list[dict], bm25_chunks: list[dict], k: int) -> list[dict]:
    """Reciprocal Rank Fusion: score = 1/(RRF_K + rank) summed across both lists."""
    scores: dict[int, float] = {}
    chunk_by_index: dict[int, dict] = {}

    for rank, chunk in enumerate(semantic_chunks):
        idx = chunk["chunk_index"]
        scores[idx] = scores.get(idx, 0.0) + 1.0 / (RRF_K + rank + 1)
        chunk_by_index[idx] = chunk

    for rank, chunk in enumerate(bm25_chunks):
        idx = chunk["chunk_index"]
        scores[idx] = scores.get(idx, 0.0) + 1.0 / (RRF_K + rank + 1)
        chunk_by_index[idx] = chunk

    ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:k]
    return [chunk_by_index[idx] for idx, _ in ranked]


def _build_context(chunks: list[dict]) -> str:
    parts = [f"[{chunk['source']}]\n{chunk['text']}" for chunk in chunks]
    return "\n\n---\n\n".join(parts)


def _extract_course_codes(text: str) -> list[str]:
    """Extract UCI course codes like CS 161, ICS 32, CS 178A from text."""
    import re
    return re.findall(r'\b(?:CS|ICS|INF|COMPSCI)\s*\d+[A-Z]?\b', text, re.IGNORECASE)


def _filter_chunks_for_followup(chunks: list[dict], last_answer: str) -> list[dict]:
    """
    When the user asks a follow-up, filter retrieved chunks to those that mention
    the same courses as the prior answer. Falls back to all chunks if none match,
    so a refusal is never triggered by over-filtering.
    """
    codes = _extract_course_codes(last_answer)
    if not codes:
        return chunks
    codes_upper = [c.upper().replace(" ", "") for c in codes]
    filtered = [
        c for c in chunks
        if any(code in c["text"].upper().replace(" ", "") for code in codes_upper)
    ]
    return filtered if filtered else chunks


def ask(
    question: str,
    k: int = TOP_K,
    use_hybrid: bool = True,
    source_filter: list[str] | None = None,
    history: list[dict] | None = None,
) -> dict:
    """
    Run the full RAG pipeline for a question.

    history is a list of prior {"role": "user"/"assistant", "content": str} turns.
    Fresh context is retrieved and injected only for the current question; prior
    turns provide conversational continuity without re-injecting their context.

    Returns {"answer": str, "sources": list[str], "chunks": list[dict],
             "retrieval_method": str}
    """
    model, collection, groq_client = _load_resources()

    semantic_chunks = _retrieve_semantic(question, model, collection, k, source_filter)

    if use_hybrid:
        bm25_chunks = _retrieve_bm25(question, k, source_filter)
        chunks = _rrf_merge(semantic_chunks, bm25_chunks, k)
        retrieval_method = "hybrid (semantic + BM25, RRF merge)"
    else:
        chunks = semantic_chunks
        retrieval_method = "semantic only"

    # For follow-up questions, filter retrieved chunks to those mentioning prior courses
    if history:
        last_answer = next(
            (m["content"] for m in reversed(history) if m["role"] == "assistant"), ""
        )
        chunks = _filter_chunks_for_followup(chunks, last_answer)

    if source_filter:
        retrieval_method += f" | filtered to {len(source_filter)} source(s)"

    context = _build_context(chunks)

    if history:
        last_answer = next(
            (m["content"] for m in reversed(history) if m["role"] == "assistant"), ""
        )
        user_message = (
            f"Context documents:\n\n{context}\n\n---\n\n"
            f"Your previous response was:\n{last_answer}\n\n"
            f"The user is asking a follow-up question. "
            f"Answer ONLY about the specific courses, professors, or topics you mentioned "
            f"in your previous response above. Do not introduce anything new.\n\n"
            f"Follow-up question: {question}"
        )
    else:
        user_message = f"Context documents:\n\n{context}\n\n---\n\nQuestion: {question}"

    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    if history:
        messages.extend(history)
    messages.append({"role": "user", "content": user_message})

    response = groq_client.chat.completions.create(
        model=GROQ_MODEL,
        messages=messages,
        temperature=0.2,
    )

    answer = response.choices[0].message.content.strip()

    if REFUSAL_PHRASE in answer:
        return {"answer": answer, "sources": [], "chunks": chunks, "retrieval_method": retrieval_method}

    seen: set[str] = set()
    sources: list[str] = []
    for chunk in chunks:
        src = chunk["source"]
        if src not in seen and src in answer:
            seen.add(src)
            sources.append(src)

    return {"answer": answer, "sources": sources, "chunks": chunks, "retrieval_method": retrieval_method}


if __name__ == "__main__":
    test_queries = [
        "What are some upper-div project-based courses that are considered easy?",
        "Who is the best professor for ICS 32? I want someone with engaging lectures who doesn't grade hard.",
        "What is the weather like in Irvine?",  # out-of-scope — should refuse
    ]

    for question in test_queries:
        print(f"\n{'='*70}")
        print(f"Q: {question}")

        semantic = ask(question, use_hybrid=False)
        hybrid = ask(question, use_hybrid=True)

        print(f"\n--- SEMANTIC ONLY ---")
        print(semantic["answer"])
        sem_srcs = [f"  [{c['source']} dist={c.get('distance','?')}]" for c in semantic["chunks"]]
        print("Retrieved:\n" + "\n".join(sem_srcs))

        print(f"\n--- HYBRID (BM25 + Semantic, RRF) ---")
        print(hybrid["answer"])
        hyb_srcs = [f"  [{c['source']}]" for c in hybrid["chunks"]]
        print("Retrieved:\n" + "\n".join(hyb_srcs))

        same = set(c["source"] for c in semantic["chunks"]) == set(c["source"] for c in hybrid["chunks"])
        print(f"\nSame top-{TOP_K} sources? {'yes' if same else 'NO — hybrid retrieved different chunks'}")
