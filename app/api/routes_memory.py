from __future__ import annotations
from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from app.memory_service import MemoryService
from dream.models import EpisodicUnit, EpisodeProposal

router = APIRouter()

# Instância única pro exemplo.
# Em produção, poderia ser injetado via Depends e ciclo de vida.
memory_service = MemoryService()


# --------- SCHEMAS Pydantic (DTOs) ---------

class InteractionIn(BaseModel):
    input_text: str
    output_text: str
    metadata: Optional[dict] = None


class EpisodeProposalOut(BaseModel):
    user_id: str
    summary: str
    topic: Optional[str] = None


class EpisodeConfirmIn(BaseModel):
    user_id: str
    summary: str
    topic: Optional[str] = None
    importance_score: Optional[float] = None
    confirmed: bool


class EpisodicUnitOut(BaseModel):
    episode_id: str
    summary: str
    topic: Optional[str]
    visits: int
    ttl: str
    importance_score: Optional[float]


class ContextResponse(BaseModel):
    episodes: List[EpisodicUnitOut]


# --------- ROTAS ---------

@router.post("/users/{user_id}/interactions")
def record_interaction(user_id: str, body: InteractionIn):
    """
    Registra uma interação user <-> IA no buffer episódico DREAM.
    """
    memory_service.configure_user(user_id, opted_in=True)  # default, idempotente
    memory_service.record_interaction(
        user_id=user_id,
        input_text=body.input_text,
        output_text=body.output_text,
        metadata=body.metadata,
    )
    return {"status": "ok"}


@router.post("/users/{user_id}/episodes/propose", response_model=EpisodeProposalOut)
def propose_episode(user_id: str, topic: Optional[str] = None):
    """
    Constrói uma proposta de Episodic Unit (EU) com base no buffer atual.
    Esse é o momento em que a UI poderia perguntar ao usuário:
    'Quer salvar essa memória?'
    """
    if not memory_service.should_propose_episode(user_id):
        raise HTTPException(status_code=400, detail="No episode to propose yet.")

    proposal: Optional[EpisodeProposal] = memory_service.build_episode_proposal(
        user_id=user_id,
        topic=topic,
    )
    if proposal is None:
        raise HTTPException(status_code=400, detail="No proposal built.")

    # Aqui estou devolvendo só resumo básico; na prática você poderia devolver mais.
    return EpisodeProposalOut(
        user_id=proposal.user_id,
        summary=proposal.summary,
        topic=proposal.topic,
    )


@router.post("/users/{user_id}/episodes/confirm", response_model=Optional[EpisodicUnitOut])
def confirm_episode(user_id: str, body: EpisodeConfirmIn):
    """
    Recebe a decisão do usuário sobre salvar ou não a memória.
    Obs: aqui simplifiquei: na prática, você atrelaria isso a um ID da proposta.
    """
    # Como exemplo, reconstruímos uma nova proposta só usando summary.
    # Em um sistema real, você manteria a proposta em cache ou storage.
    # Aqui, vamos assumir que acabou de ser proposta e estamos confirmando.
    proposal = EpisodeProposal(
        user_id=user_id,
        events=[],
        summary=body.summary,
        embedding=memory_service._orchestrator.embedder.embed(body.summary),
        topic=body.topic,
    )

    eu = memory_service.confirm_episode(
        proposal=proposal,
        user_confirmed=body.confirmed,
        importance_score=body.importance_score,
    )

    if not eu:
        # episódio descartado
        return None

    return EpisodicUnitOut(
        episode_id=eu.episode_id,
        summary=eu.summary,
        topic=eu.topic,
        visits=eu.visits,
        ttl=eu.ttl.isoformat(),
        importance_score=eu.importance_score,
    )


@router.get("/users/{user_id}/context", response_model=ContextResponse)
def retrieve_context(user_id: str, query: str, top_k: int = 5):
    """
    Recupera episódios relevantes para a query.
    Implementa o fluxo:
      - embed da query
      - busca vetorial por user_id
      - ARM.on_reuse em cada EU usado
    """
    eus = memory_service.retrieve_context(
        user_id=user_id,
        query_text=query,
        top_k=top_k,
    )

    return ContextResponse(
        episodes=[
            EpisodicUnitOut(
                episode_id=eu.episode_id,
                summary=eu.summary,
                topic=eu.topic,
                visits=eu.visits,
                ttl=eu.ttl.isoformat(),
                importance_score=eu.importance_score,
            )
            for eu in eus
        ]
    )
