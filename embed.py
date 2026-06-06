import json
from pathlib import Path

import chromadb
from sentence_transformers import SentenceTransformer

from ingest import DOCUMENTS_DIR, chunk_documents, clean, load_documents

CHROMA_PATH = Path(__file__).parent / "chroma_db"
CHUNKS_PATH = Path(__file__).parent / "chunks.json"
COLLECTION_NAME = "uci_cs_guide"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
TOP_K = 5


def build_index(chunks: list[dict], model: SentenceTransformer) -> chromadb.Collection:
    client = chromadb.PersistentClient(path=str(CHROMA_PATH))

    # Drop and recreate so re-runs start clean
    try:
        client.delete_collection(COLLECTION_NAME)
    except Exception:
        pass
    collection = client.create_collection(
        COLLECTION_NAME,
        metadata={"hnsw:space": "cosine"},  # cosine distance for sentence-transformers
    )

    texts = [c["text"] for c in chunks]
    print(f"  Embedding {len(texts)} chunks with {EMBEDDING_MODEL}...")
    embeddings = model.encode(texts, show_progress_bar=True, batch_size=64)

    collection.add(
        ids=[str(i) for i in range(len(chunks))],
        embeddings=embeddings.tolist(),
        documents=texts,
        metadatas=[
            {"source": c["source"], "chunk_index": i}
            for i, c in enumerate(chunks)
        ],
    )

    CHUNKS_PATH.write_text(
        json.dumps(chunks, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(f"  Saved {len(chunks)} chunks to {CHUNKS_PATH}")

    print(f"  Stored {collection.count()} chunks in ChromaDB at {CHROMA_PATH}")
    return collection


def retrieve(
    query: str,
    collection: chromadb.Collection,
    model: SentenceTransformer,
    k: int = TOP_K,
) -> list[dict]:
    query_embedding = model.encode([query])[0]
    results = collection.query(
        query_embeddings=[query_embedding.tolist()],
        n_results=k,
        include=["documents", "metadatas", "distances"],
    )
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


def main():
    # ── Ingest ──────────────────────────────────────────────────────────────
    print("Loading and chunking documents...")
    documents = load_documents(DOCUMENTS_DIR)
    for doc in documents:
        doc["text"] = clean(doc["text"])
    chunks = chunk_documents(documents)
    print(f"  {len(chunks)} chunks ready\n")

    # ── Embed & store ────────────────────────────────────────────────────────
    print(f"Loading embedding model: {EMBEDDING_MODEL}")
    model = SentenceTransformer(EMBEDDING_MODEL)

    print("\nBuilding ChromaDB index...")
    collection = build_index(chunks, model)

    # ── Retrieval smoke test ─────────────────────────────────────────────────
    test_queries = [
        "What are some upper-div project-based courses that are considered easy?",
        "Who is the best professor for ICS 32?",
        "Which electives are recommended for students interested in machine learning?",
    ]

    print("\n" + "=" * 70)
    print("RETRIEVAL TEST  (cosine distance: lower = more similar)")
    print("Good result: distance < 0.5  |  Weak result: distance > 0.6")
    print("=" * 70)

    for query in test_queries:
        print(f"\nQuery: {query}\n")
        for i, chunk in enumerate(retrieve(query, collection, model), 1):
            preview = chunk["text"][:300].strip().encode("ascii", errors="replace").decode("ascii")
            print(f"  [{i}] distance={chunk['distance']}  source={chunk['source']}")
            print(f"      {preview}")
            print()

    return collection, model


if __name__ == "__main__":
    main()
