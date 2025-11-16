from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional

@dataclass
class MemoryEvent:
    user_id: str
    timestamp: datetime
    input_text: str
    output_text: str
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class EpisodicUnit:
    user_id: str
    episode_id: str
    summary: str
    embedding: List[float]
    timestamp: datetime
    ttl: datetime
    visits: int = 0
    topic: Optional[str] = None
    importance_score: Optional[float] = None

    def is_expired(self, now: Optional[datetime] = None) -> bool:
        from datetime import datetime as _dt
        now = now or _dt.utcnow()
        return now >= self.ttl


@dataclass
class UserMemoryConfig:
    user_id: str
    opted_in: bool = True
    max_buffer_events: int = 8
    max_buffer_age_sec: int = 600


@dataclass
class EpisodeProposal:
    user_id: str
    events: List[MemoryEvent]
    summary: str
    embedding: List[float]
    topic: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.utcnow)
