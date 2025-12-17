from models.model import faiss_index, save_faiss_index


def persist_memory():
    save_faiss_index(faiss_index)
