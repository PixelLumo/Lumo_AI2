import os
import pickle
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
import requests
from dotenv import load_dotenv

load_dotenv()

# Config
LOCAL_MODEL = int(os.getenv("LOCAL_MODEL", 1))
FAISS_DIM = int(os.getenv("FAISS_DIM", 384))
FAISS_INDEX_PATH = os.getenv("FAISS_INDEX_PATH", "memory/faiss_index.pkl")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"


def load_faiss_index():
    if os.path.exists(FAISS_INDEX_PATH):
        with open(FAISS_INDEX_PATH, "rb") as f:
            index = pickle.load(f)
    else:
        index = faiss.IndexFlatL2(FAISS_DIM)
    return index


def save_faiss_index(index):
    with open(FAISS_INDEX_PATH, "wb") as f:
        pickle.dump(index, f)


# Embedding model
embedder = SentenceTransformer("all-MiniLM-L6-v2")
faiss_index = load_faiss_index()
faiss_texts = []  # Keep actual texts to return


def add_to_index(texts):
    embeddings = embedder.encode(texts)
    faiss_index.add(np.array(embeddings, dtype=np.float32))
    faiss_texts.extend(texts)
    save_faiss_index(faiss_index)
    # Save texts alongside FAISS
    with open("memory/faiss_texts.pkl", "wb") as f:
        pickle.dump(faiss_texts, f)


# Load texts
if os.path.exists("memory/faiss_texts.pkl"):
    with open("memory/faiss_texts.pkl", "rb") as f:
        faiss_texts = pickle.load(f)


def search_index(query, top_k=3):
    query_vec = embedder.encode([query])
    distances, indices = faiss_index.search(
        np.array(query_vec, dtype=np.float32), top_k
    )
    results = [faiss_texts[i] if i != -1 else None for i in indices[0]]
    return results


def generate_response(prompt):
    try:
        if LOCAL_MODEL:
            hits = search_index(prompt)
            if hits and hits[0]:
                return f"Local FAISS hit: {hits[0]}"
            raise Exception("No local FAISS matches")
    except Exception:
        # Fallback to OpenAI
        headers = {"Authorization": f"Bearer {OPENAI_API_KEY}"}
        json_data = {
            "model": "gpt-4o-mini",
            "messages": [{"role": "user", "content": prompt}],
        }
        r = requests.post(OPENAI_API_URL, headers=headers, json=json_data)
        return r.json()["choices"][0]["message"]["content"]
