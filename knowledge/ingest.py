import os
import json

RAW_DIR = "knowledge/raw"
OUT_FILE = "knowledge/chunks.jsonl"


def chunk_text(text, size=500, overlap=50):
    """Split text into overlapping chunks for semantic search."""
    chunks = []
    start = 0
    while start < len(text):
        end = start + size
        chunk = text[start:end]
        chunks.append(chunk)
        start += size - overlap
    return chunks


def ingest():
    """Read raw documents and chunk them into JSONL."""
    with open(OUT_FILE, "w", encoding="utf-8") as out:
        for fname in os.listdir(RAW_DIR):
            path = os.path.join(RAW_DIR, fname)
            if not fname.endswith(".txt"):
                continue

            with open(path, encoding="utf-8") as f:
                text = f.read()

            for i, chunk in enumerate(chunk_text(text)):
                out.write(json.dumps({
                    "source": fname,
                    "id": f"{fname}:{i}",
                    "text": chunk
                }) + "\n")

    print(f"Knowledge chunked → {OUT_FILE}")


if __name__ == "__main__":
    ingest()
