"""
Chunking Strategy Comparison
Builds a temporary in-memory ChromaDB collection for each strategy,
runs the same query set, and reports retrieval quality metrics.
No Groq API calls — pure retrieval evaluation.
"""

from dataclasses import dataclass

import chromadb
from langchain_text_splitters import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer

from ingest import DOCUMENTS_DIR, clean, load_documents

EMBEDDING_MODEL = "all-MiniLM-L6-v2"
TOP_K = 5

TEST_QUERIES = [
    "What are some easy upper-division project-based CS courses?",
    "Who teaches ICS 32 and what do students think of them?",
    "What CS electives are recommended for students interested in machine learning?",
    "What are the lower division requirements for the CS major?",
    "Which courses are considered high workload or difficult?",
]


@dataclass
class Strategy:
    name: str
    chunk_size: int
    chunk_overlap: int
    description: str


STRATEGIES = [
    Strategy("Small",  400,  50, "More chunks, higher precision, less context per chunk"),
    Strategy("Medium", 800, 100, "Baseline — current production setting"),
    Strategy("Large", 1200, 150, "Fewer chunks, more context per chunk, risk of dilution"),
]


def chunk_documents(documents: list[dict], strategy: Strategy) -> list[dict]:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=strategy.chunk_size,
        chunk_overlap=strategy.chunk_overlap,
        separators=["\n\n", "\n", " ", ""],
    )
    chunks = []
    for doc in documents:
        for split in splitter.split_text(doc["text"]):
            chunks.append({"source": doc["source"], "text": split})
    return chunks


def build_collection(
    chunks: list[dict], model: SentenceTransformer, collection_name: str
) -> chromadb.Collection:
    client = chromadb.Client()  # in-memory, discarded after script exits
    collection = client.create_collection(
        collection_name, metadata={"hnsw:space": "cosine"}
    )
    texts = [c["text"] for c in chunks]
    embeddings = model.encode(texts, show_progress_bar=False, batch_size=64)
    collection.add(
        ids=[str(i) for i in range(len(chunks))],
        embeddings=embeddings.tolist(),
        documents=texts,
        metadatas=[{"source": c["source"]} for c in chunks],
    )
    return collection


def retrieve(query: str, collection: chromadb.Collection, model: SentenceTransformer) -> list[dict]:
    embedding = model.encode([query])[0]
    results = collection.query(
        query_embeddings=[embedding.tolist()],
        n_results=TOP_K,
        include=["metadatas", "distances"],
    )
    return [
        {"source": meta["source"], "distance": dist}
        for meta, dist in zip(results["metadatas"][0], results["distances"][0])
    ]


@dataclass
class StrategyResult:
    strategy: Strategy
    num_chunks: int
    avg_distance: float
    unique_sources: set[str]
    per_query: list[list[dict]]  # [query_idx][chunk_idx]


def evaluate(
    strategy: Strategy, documents: list[dict], model: SentenceTransformer
) -> StrategyResult:
    chunks = chunk_documents(documents, strategy)
    collection = build_collection(chunks, model, f"eval_{strategy.name.lower()}")

    all_distances: list[float] = []
    all_sources: set[str] = set()
    per_query: list[list[dict]] = []

    for query in TEST_QUERIES:
        results = retrieve(query, collection, model)
        per_query.append(results)
        for r in results:
            all_distances.append(r["distance"])
            all_sources.add(r["source"])

    avg_dist = sum(all_distances) / len(all_distances)
    return StrategyResult(strategy, len(chunks), round(avg_dist, 4), all_sources, per_query)


def print_report(results: list[StrategyResult]) -> None:
    sep = "=" * 70

    print(f"\n{sep}")
    print("CHUNKING STRATEGY COMPARISON")
    print(f"Queries tested: {len(TEST_QUERIES)}  |  Top-K: {TOP_K}")
    print(f"Metric: cosine distance (lower = more similar to query)")
    print(sep)

    # Summary table
    print(f"\n{'Strategy':<10}  {'Chunks':>7}  {'Avg Dist':>9}  {'Unique Sources':>15}  Description")
    print("-" * 70)
    for r in results:
        print(
            f"{r.strategy.name:<10}  {r.num_chunks:>7}  {r.avg_distance:>9.4f}"
            f"  {len(r.unique_sources):>15}  {r.strategy.description}"
        )

    # Winner
    best = min(results, key=lambda r: r.avg_distance)
    print(f"\nBest average retrieval distance: {best.strategy.name} ({best.avg_distance})")

    # Per-query breakdown
    print(f"\n{sep}")
    print("PER-QUERY DISTANCE BREAKDOWN")
    print(sep)
    header = f"{'Query':<50}" + "".join(f"  {r.strategy.name:>8}" for r in results)
    print(header)
    print("-" * 70)
    for q_idx, query in enumerate(TEST_QUERIES):
        row = f"{query[:48]:<50}"
        for r in results:
            avg = sum(x["distance"] for x in r.per_query[q_idx]) / TOP_K
            row += f"  {avg:>8.4f}"
        print(row)

    # Source overlap analysis
    print(f"\n{sep}")
    print("SOURCE DIVERSITY (unique source files surfaced per strategy)")
    print(sep)
    for r in results:
        print(f"\n{r.strategy.name} ({len(r.unique_sources)} unique sources):")
        for src in sorted(r.unique_sources):
            print(f"  • {src}")

    # Recommendation
    print(f"\n{sep}")
    print("RECOMMENDATION")
    print(sep)
    scores = {r.strategy.name: r.avg_distance for r in results}
    ranked = sorted(scores.items(), key=lambda x: x[1])
    print(f"Ranked by average distance (best first):")
    for name, score in ranked:
        r = next(x for x in results if x.strategy.name == name)
        print(f"  {name}: {score}  ({r.num_chunks} chunks)")

    winner = results[ranked.index(min(ranked, key=lambda x: x[1]))]
    runner_up = results[1] if winner == results[0] else results[0]
    improvement = round(runner_up.avg_distance - winner.avg_distance, 4)
    print(
        f"\n{winner.strategy.name} chunks win with avg distance {winner.avg_distance} "
        f"({improvement} better than runner-up)."
    )
    print(
        f"Tradeoff: {winner.strategy.name} produces {winner.num_chunks} chunks "
        f"vs {runner_up.num_chunks} for {runner_up.strategy.name}."
    )


def main():
    print("Loading and cleaning documents...")
    documents = load_documents(DOCUMENTS_DIR)
    for doc in documents:
        doc["text"] = clean(doc["text"])
    print(f"  {len(documents)} documents loaded")

    print(f"\nLoading embedding model: {EMBEDDING_MODEL}")
    model = SentenceTransformer(EMBEDDING_MODEL)

    results: list[StrategyResult] = []
    for strategy in STRATEGIES:
        print(f"\nEvaluating {strategy.name} strategy (chunk_size={strategy.chunk_size}, overlap={strategy.chunk_overlap})...")
        result = evaluate(strategy, documents, model)
        results.append(result)
        print(f"  {result.num_chunks} chunks, avg_distance={result.avg_distance}, unique_sources={len(result.unique_sources)}")

    print_report(results)


if __name__ == "__main__":
    main()
