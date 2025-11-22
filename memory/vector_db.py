import chromadb
import random
from typing import List

class VectorDB:
    """
    Manages the vector index (ChromaDB wrapper).
    """
    def __init__(self):
        # Creates a volatile vector DB (in-memory) for quick testing
        self.client = chromadb.Client()
        self.collection = self.client.create_collection("dream_memory_v2")

    def add_vector(self, memory_id: str, embedding: List[float], metadata: dict):
        self.collection.add(
            ids=[memory_id],
            embeddings=[embedding],
            metadatas=[metadata]
        )

    def search(self, query_embedding: List[float], n_results=3):
        return self.collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results
        )

    @staticmethod
    def get_mock_embedding(dim=384) -> List[float]:
        """
        Generates a random vector to simulate AI embeddings without API costs.
        In production, replace with OpenAI/HuggingFace embeddings.
        """
        return [random.random() for _ in range(dim)]