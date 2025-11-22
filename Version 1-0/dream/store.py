from __future__ import annotations
from typing import Dict, List, Tuple, Optional
from datetime import datetime
from .models import EpisodicUnit
from .interfaces import VectorStore
from .embedding import cosine_similarity

class InMemoryVectorStore(VectorStore):
    """
    In-memory vector index, separated by user_id.
    Good for demos and tests.
    """
    def __init__(self):
        self._by_user: Dict[str, List[EpisodicUnit]] = {}

    def add_eu(self, eu: EpisodicUnit) -> None:
        self._by_user.setdefault(eu.user_id, []).append(eu)

    def query(
        self,
        user_id: str,
        query_embedding,
        top_k: int = 5,
        now: Optional[datetime] = None,
    ) -> List[Tuple[EpisodicUnit, float]]:
        now = now or datetime.utcnow()
        bucket = self._by_user.get(user_id, [])
        results: List[Tuple[EpisodicUnit, float]] = []

        for eu in bucket:
            if eu.is_expired(now):
                continue
            sim = cosine_similarity(eu.embedding, query_embedding)
            results.append((eu, sim))

        results.sort(key=lambda x: x[1], reverse=True)
        return results[:top_k]

    def delete_expired(self, now: Optional[datetime] = None) -> None:
        now = now or datetime.utcnow()
        for user_id, bucket in list(self._by_user.items()):
            self._by_user[user_id] = [
                eu for eu in bucket if not eu.is_expired(now)
            ]
