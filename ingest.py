import re
from pathlib import Path

from langchain_text_splitters import RecursiveCharacterTextSplitter

DOCUMENTS_DIR = Path(__file__).parent / "documents"
CHUNK_SIZE = 800
CHUNK_OVERLAP = 100


def load_documents(docs_dir: Path) -> list[dict]:
    documents = []
    for path in sorted(docs_dir.glob("*.txt")):
        text = path.read_text(encoding="utf-8")
        documents.append({"source": path.name, "text": text})
    return documents


def clean(text: str) -> str:
    # Normalize unicode whitespace
    text = text.replace("\xa0", " ").replace("​", "")

    # Remove course offerings UI navigation lines
    text = re.sub(r"^Search (titles|Fall|Winter|Spring)\s*$", "", text, flags=re.MULTILINE)

    # Remove schedule page boilerplate banner lines (rows of # characters)
    text = re.sub(r"^[ \t#]{10,}\n", "", text, flags=re.MULTILINE)

    # Collapse 3+ blank lines to 2
    text = re.sub(r"\n{3,}", "\n\n", text)

    # Strip trailing whitespace from each line
    text = "\n".join(line.rstrip() for line in text.splitlines())

    return text.strip()


def chunk_documents(documents: list[dict]) -> list[dict]:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=["\n\n", "\n", " ", ""],
    )

    chunks = []
    for doc in documents:
        for split in splitter.split_text(doc["text"]):
            chunks.append({"source": doc["source"], "text": split})
            
    return chunks


def main():
    print("Loading documents...")
    documents = load_documents(DOCUMENTS_DIR)
    print(f"  Loaded {len(documents)} files")

    print("\nCleaning documents...")
    for doc in documents:
        doc["text"] = clean(doc["text"])

    print(f"\n--- First document after cleaning: {documents[0]['source']} ---")
    print(documents[0]["text"][:600])
    print("---")

    print("\nChunking documents...")
    chunks = chunk_documents(documents)
    print(f"  Total chunks: {len(chunks)}")

    print("\n--- 5 representative chunks ---")
    step = max(1, len(chunks) // 5)
    for i, idx in enumerate([0, step, step * 2, step * 3, len(chunks) - 1], 1):
        chunk = chunks[idx]
        print(f"\nChunk {i} (index {idx}, source: {chunk['source']}, {len(chunk['text'])} chars):")
        print("-" * 60)
        print(chunk["text"])
        print("-" * 60)

    print(f"\nTotal chunks: {len(chunks)}")
    if len(chunks) < 50:
        print("WARNING: Fewer than 50 chunks — chunk size may be too large.")
    elif len(chunks) > 2000:
        print("WARNING: More than 2000 chunks — chunk size may be too small.")
    else:
        print("Chunk count is in a healthy range (50–2000).")

    return chunks


if __name__ == "__main__":
    main()
