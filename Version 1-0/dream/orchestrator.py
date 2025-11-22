from __future__ import annotations
from datetime import datetime
from typing import Dict, List, Optional
from .models import (
    MemoryEvent,
    EpisodicUnit,
    UserMemoryConfig,
    EpisodeProposal,
)
from .interfaces import Summarizer, Embedder, VectorStore
from .arm import AdaptiveRetentionMechanism

class DreamOrchestrator:
    """
    Core of the DREAM pattern:
    - event buffer per user
    - EpisodicUnit proposal
    - opt-in per episode
    - ARM (adaptive TTL) on revisits
    """

    def __init__(
        self,
        summarizer: Summarizer,
        embedder: Embedder,
        vector_store: VectorStore,
        arm: Optional[AdaptiveRetentionMechanism] = None,
    ):
        self.summarizer = summarizer
        self.embedder = embedder
        self.vector_store = vector_store
        self.arm = arm or AdaptiveRetentionMechanism()

        self._buffers: Dict[str, List[MemoryEvent]] = {}
        self._configs: Dict[str, UserMemoryConfig] = {}

    # ---------------- CONFIG USER ----------------

    def configure_user(
        self,
        user_id: str,
        opted_in: bool = True,
        max_buffer_events: int = 8,
        max_buffer_age_sec: int = 600,
    ) -> None:
        self._configs[user_id] = UserMemoryConfig(
            user_id=user_id,
            opted_in=opted_in,
            max_buffer_events=max_buffer_events,
            max_buffer_age_sec=max_buffer_age_sec,
        )

    def set_opt_in(self, user_id: str, opted_in: bool) -> None:
        cfg = self._configs.get(user_id)
        if cfg is None:
            cfg = UserMemoryConfig(user_id=user_id, opted_in=opted_in)
            self._configs[user_id] = cfg
        else:
            cfg.opted_in = opted_in

    def _get_config(self, user_id: str) -> UserMemoryConfig:
        if user_id not in self._configs:
            self._configs[user_id] = UserMemoryConfig(user_id=user_id)
        return self._configs[user_id]

    # ---------------- EVENTS ----------------

    def record_interaction(
        self,
        user_id: str,
        input_text: str,
        output_text: str,
        metadata: Optional[dict] = None,
        now: Optional[datetime] = None,
    ) -> None:
        now = now or datetime.utcnow()
        cfg = self._get_config(user_id)
        if not cfg.opted_in:
            return

        ev = MemoryEvent(
            user_id=user_id,
            timestamp=now,
            input_text=input_text,
            output_text=output_text,
            metadata=metadata or {},
        )
        buf = self._buffers.setdefault(user_id, [])
        buf.append(ev)

    def _get_buffer_age_sec(self, user_id: str, now: datetime) -> float:
        buf = self._buffers.get(user_id, [])
        if not buf:
            return 0.0
        first_ts = buf[0].timestamp
        return (now - first_ts).total_seconds()

    def should_propose_episode(self, user_id: str, now: Optional[datetime] = None) -> bool:
        now = now or datetime.utcnow()
        cfg = self._get_config(user_id)
        buf = self._buffers.get(user_id, [])
        if not buf:
            return False
        if len(buf) >= cfg.max_buffer_events:
            return True
        if self._get_buffer_age_sec(user_id, now) >= cfg.max_buffer_age_sec:
            return True
        return False

    # ---------------- EPISODE (PROPOSAL + CONFIRMATION) ----------------

    def build_episode_proposal(
        self,
        user_id: str,
        topic: Optional[str] = None,
        now: Optional[datetime] = None,
    ) -> Optional[EpisodeProposal]:
        now = now or datetime.utcnow()
        cfg = self._get_config(user_id)
        if not cfg.opted_in:
            return None

        buf = self._buffers.get(user_id, [])
        if not buf:
            return None

        summary = self.summarizer.summarize(buf)
        emb = self.embedder.embed(summary)

        proposal = EpisodeProposal(
            user_id=user_id,
            events=list(buf),
            summary=summary,
            embedding=emb,
            topic=topic,
            created_at=now,
        )

        # this segment has been "closed"
        self._buffers[user_id] = []
        return proposal

    def confirm_episode(
        self,
        proposal: EpisodeProposal,
        user_confirmed: bool,
        importance_score: Optional[float] = None,
        now: Optional[datetime] = None,
    ) -> Optional[EpisodicUnit]:
        if not user_confirmed:
            return None

        now = now or datetime.utcnow()
        eu = EpisodicUnit(
            user_id=proposal.user_id,
            episode_id=f"eu_{now.timestamp()}",
            summary=proposal.summary,
            embedding=proposal.embedding,
            timestamp=proposal.created_at,
            ttl=now,  # ARM vai ajustar
            visits=0,
            topic=proposal.topic,
            importance_score=importance_score,
        )
        self.arm.initialize_eu(eu, now)
        self.vector_store.add_eu(eu)
        return eu

    # ---------------- RETRIEVAL ----------------

    def retrieve_context(
        self,
        user_id: str,
        query_text: str,
        top_k: int = 5,
        now: Optional[datetime] = None,
    ) -> List[EpisodicUnit]:
        now = now or datetime.utcnow()
        cfg = self._get_config(user_id)
        if not cfg.opted_in:
            return []

        query_emb = self.embedder.embed(query_text)
        results = self.vector_store.query(
            user_id=user_id,
            query_embedding=query_emb,
            top_k=top_k,
            now=now,
        )

        eus: List[EpisodicUnit] = []
        for eu, _sim in results:
            self.arm.on_reuse(eu, now)
            eus.append(eu)
        return eus

    # ---------------- MAINTENANCE ----------------

    def prune_expired(self, now: Optional[datetime] = None) -> None:
        self.vector_store.delete_expired(now=now)


def shard_for_user(user_id: str, total_shards: int) -> int:
    return hash(user_id) % total_shards
