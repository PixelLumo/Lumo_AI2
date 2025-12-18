import faiss
import numpy as np


class Memory:
    def __init__(self, dim=1536):
        self.index = faiss.IndexFlatL2(dim)
        self.data = []

    def add(self, embedding, text):
        self.index.add(np.array([embedding]).astype("float32"))
        self.data.append(text)

    def search(self, embedding, k=3):
        if self.index.ntotal == 0:
            return []
        distances, indices = self.index.search(
            np.array([embedding]).astype("float32"), k
        )
        return [self.data[i] for i in indices[0]]
