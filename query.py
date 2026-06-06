import os
from pathlib import Path

import chromadb
from dotenv import load_dotenv
from groq import Groq
from sentence_transformers import SentenceTransformer

load_dotenv()

CHROMA_PATH = Path(__file__).parent / "chroma_db"
COLLECTION_NAME = "uci_cs_guide"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
GROQ_MODEL = "llama-3.3-70b-versatile"
TOP_K = 5

REFUSAL_PHRASE = "I don't have enough information on that based on the available documents."

SYSTEM_PROMPT = f"""You are a helpful assistant for UCI Computer Science students planning their courses.

Answer questions ONLY using the information in the context documents provided below.
Do NOT use any outside knowledge, training data, or general information — even if you are confident about the answer.
If the context documents do not contain enough information to answer the question, respond with exactly:
"{REFUSAL_PHRASE}"

Do not make assumptions or inferences beyond what is explicitly stated in the documents.
Be specific: quote or paraphrase the relevant parts of the documents in your answer.
Always include citations. When citing information, refer to the source by its filename as it appears in the document header (e.g. "According to rate_my_professor.txt..." or "A student on low_stress_cs_electives.txt noted...")."""

# Module-level singletons — loaded once, reused across all queries
_model: SentenceTransformer | None = None
_collection: chromadb.Collection | None = None
_client: Groq | None = None


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


def _retrieve(query: str, model: SentenceTransformer, collection: chromadb.Collection, k: int) -> list[dict]:
    embedding = model.encode([query])[0]
    results = collection.query(
        query_embeddings=[embedding.tolist()],
        n_results=k,
        include=["documents", "metadatas", "distances"],
    )
    return [
        {
            "text": doc,
            "source": meta["source"],
            "distance": round(dist, 4),
        }
        for doc, meta, dist in zip(
            results["documents"][0],
            results["metadatas"][0],
            results["distances"][0],
        )
    ]


def _build_context(chunks: list[dict]) -> str:
    parts = []
    for chunk in chunks:
        parts.append(f"[{chunk['source']}]\n{chunk['text']}")
    return "\n\n---\n\n".join(parts)


def ask(question: str, k: int = TOP_K) -> dict:
    """
    Run the full RAG pipeline for a question.
    Returns {"answer": str, "sources": list[str], "chunks": list[dict]}
    """
    model, collection, groq_client = _load_resources()

    chunks = _retrieve(question, model, collection, k)
    context = _build_context(chunks)

    user_message = f"Context documents:\n\n{context}\n\n---\n\nQuestion: {question}"

    response = groq_client.chat.completions.create(
        model=GROQ_MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_message},
        ],
        temperature=0.2,  # low temperature = more faithful to context
    )

    answer = response.choices[0].message.content.strip()

    # Suppress sources when the model couldn't answer from context
    if REFUSAL_PHRASE in answer:
        return {"answer": answer, "sources": [], "chunks": chunks}

    # Only list sources the LLM actually cited in its answer (by filename)
    seen = set()
    sources = []
    for chunk in chunks:
        src = chunk["source"]
        if src not in seen and src in answer:
            seen.add(src)
            sources.append(src)

    return {"answer": answer, "sources": sources, "chunks": chunks}


if __name__ == "__main__":
    test_queries = [
        "What are some upper-div project-based courses that are considered easy?",
        "Who is the best professor for ICS 32? I want someone with engaging lectures who doesn't grade hard.",
        "What is the weather like in Irvine?",  # out-of-scope test — should refuse
    ]

    for question in test_queries:
        print(f"\n{'='*70}")
        print(f"Q: {question}")
        print("=" * 70)
        result = ask(question)
        print(result["answer"])
        print(f"\nSources: {', '.join(result['sources'])}")
