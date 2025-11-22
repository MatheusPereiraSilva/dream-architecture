from __future__ import annotations
from dream.store import InMemoryVectorStore
from dream.interfaces import VectorStore

def get_default_vector_store() -> VectorStore:
    """
    Factory for the default VectorStore.
    In production, you could swap it for an adapter for pgvector, Pinecone, Qdrant, etc.
    """
    return InMemoryVectorStore()
