import json
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

MODEL = SentenceTransformer("all-MiniLM-L6-v2")

# Load index and metadata on module import
try:
    index = faiss.read_index("knowledge/index.faiss")
    with open("knowledge/metadata.jsonl", encoding="utf-8") as f:
        CHUNKS = [json.loads(l) for l in f]
    READY = True
except FileNotFoundError:
    READY = False
    CHUNKS = []
    index = None


def retrieve(query, k=3):
    """
    Retrieve top-k relevant chunks from knowledge base.

    Args:
        query: User question or search term
        k: Number of chunks to return (default 3)

    Returns:
        List of relevant chunk texts
    """
    if not READY:
        return []

    # Encode query
    q_emb = MODEL.encode(query).astype("float32")

    # Search index
    D, I = index.search(np.array([q_emb]), k)

    # Return chunk texts
    results = [CHUNKS[i]["text"] for i in I[0] if i < len(CHUNKS)]
    return results


def retrieve_with_source(query, k=3):
    """
    Retrieve chunks with source metadata.

    Args:
        query: User question or search term
        k: Number of chunks to return (default 3)

    Returns:
        List of dicts with 'text' and 'source'
    """
    if not READY:
        return []

    q_emb = MODEL.encode(query).astype("float32")
    D, I = index.search(np.array([q_emb]), k)

    results = []
    for i in I[0]:
        if i < len(CHUNKS):
            results.append({
                "text": CHUNKS[i]["text"],
                "source": CHUNKS[i].get("source", "unknown"),
                "distance": float(D[0][I[0].tolist().index(i)])
            })
    return results
