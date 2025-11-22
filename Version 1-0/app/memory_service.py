from __future__ import annotations
from typing import Optional, List
from datetime import datetime
from dream.orchestrator import DreamOrchestrator
from dream.models import EpisodicUnit, EpisodeProposal
from dream.arm import AdaptiveRetentionMechanism
from .llm_clients import StubSummarizerLLM, StubEmbedderLLM
from .vector_clients import get_default_vector_store

class MemoryService:
    """
    Application layer that exposes memory use cases:
    - register interaction
    - check whether to propose an episode
    - build episode proposal
    - confirm/discard episode
    - retrieve context
    """

    def __init__(self):
        summarizer = StubSummarizerLLM()
        embedder = StubEmbedderLLM()
        vector_store = get_default_vector_store()
        arm = AdaptiveRetentionMechanism()

        self._orchestrator = DreamOrchestrator(
            summarizer=summarizer,
            embedder=embedder,
            vector_store=vector_store,
            arm=arm,
        )

    # Use case: set up user
    def configure_user(
        self,
        user_id: str,
        opted_in: bool = True,
        max_buffer_events: int = 8,
        max_buffer_age_sec: int = 600,
    ) -> None:
        self._orchestrator.configure_user(
            user_id=user_id,
            opted_in=opted_in,
            max_buffer_events=max_buffer_events,
            max_buffer_age_sec=max_buffer_age_sec,
        )

    # Use case: register interaction
    def record_interaction(
        self,
        user_id: str,
        input_text: str,
        output_text: str,
        metadata: Optional[dict] = None,
        now: Optional[datetime] = None,
    ) -> None:
        self._orchestrator.record_interaction(
            user_id=user_id,
            input_text=input_text,
            output_text=output_text,
            metadata=metadata,
            now=now,
        )

    # Use case: check if it's time to propose an episode
    def should_propose_episode(self, user_id: str) -> bool:
        return self._orchestrator.should_propose_episode(user_id)

    # Use case: build proposal (summary + embedding)
    def build_episode_proposal(
        self,
        user_id: str,
        topic: Optional[str] = None,
    ) -> Optional[EpisodeProposal]:
        return self._orchestrator.build_episode_proposal(
            user_id=user_id,
            topic=topic,
        )

    # Use case: confirm/discard episode (user opt-in)
    def confirm_episode(
        self,
        proposal: EpisodeProposal,
        user_confirmed: bool,
        importance_score: Optional[float] = None,
    ) -> Optional[EpisodicUnit]:
        return self._orchestrator.confirm_episode(
            proposal=proposal,
            user_confirmed=user_confirmed,
            importance_score=importance_score,
        )

    # Use case: retrieve relevant context
    def retrieve_context(
        self,
        user_id: str,
        query_text: str,
        top_k: int = 5,
    ) -> List[EpisodicUnit]:
        return self._orchestrator.retrieve_context(
            user_id=user_id,
            query_text=query_text,
            top_k=top_k,
        )

    # Use case: maintenance
    def prune_expired(self) -> None:
        self._orchestrator.prune_expired()
