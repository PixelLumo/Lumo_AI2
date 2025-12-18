import json
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

MODEL = SentenceTransformer("all-MiniLM-L6-v2")

CHUNKS_FILE = "knowledge/chunks.jsonl"
INDEX_FILE = "knowledge/index.faiss"
METADATA_FILE = "knowledge/metadata.jsonl"

chunks = []
embeddings = []

print("Loading chunks...")
with open(CHUNKS_FILE, encoding="utf-8") as f:
    for line in f:
        obj = json.loads(line)
        chunks.append(obj)

print(f"Encoding {len(chunks)} chunks...")
embeddings = [MODEL.encode(obj["text"]) for obj in chunks]
embeddings = np.array(embeddings).astype("float32")

print(f"Building FAISS index ({embeddings.shape[0]} x {embeddings.shape[1]})...")
index = faiss.IndexFlatL2(embeddings.shape[1])
index.add(embeddings)

faiss.write_index(index, INDEX_FILE)

# Save metadata (chunk info without embeddings)
with open(METADATA_FILE, "w", encoding="utf-8") as f:
    for obj in chunks:
        f.write(json.dumps(obj) + "\n")

print(f"✓ Index saved → {INDEX_FILE}")
print(f"✓ Metadata saved → {METADATA_FILE}")
