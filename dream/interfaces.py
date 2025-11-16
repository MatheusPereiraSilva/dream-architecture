from __future__ import annotations
from typing import List, Protocol, Tuple, Optional
from datetime import datetime
from .models import EpisodicUnit

class Summarizer(Protocol):
    def summarize(self, events) -> str:
        ...


class Embedder(Protocol):
    def embed(self, text: str) -> List[float]:
        ...


class VectorStore(Protocol):
    def add_eu(self, eu: EpisodicUnit) -> None:
        ...

    def query(
        self,
        user_id: str,
        query_embedding: List[float],
        top_k: int = 5,
        now: Optional[datetime] = None,
    ) -> List[Tuple[EpisodicUnit, float]]:
        ...

    def delete_expired(self, now: Optional[datetime] = None) -> None:
        ...
