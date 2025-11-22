from __future__ import annotations
from typing import List
from dream.interfaces import Summarizer, Embedder
from dream.models import MemoryEvent
from dream.embedding import BagOfWordsEmbedder

class StubSummarizerLLM(Summarizer):
    """
    Summary LLM Adapter.
    Here you could call OpenAI, Ollama, etc.
    For now, it just joins the texts simply.
    """

    def __init__(self, max_chars: int = 800):
        self.max_chars = max_chars

    def summarize(self, events: List[MemoryEvent]) -> str:
        parts: List[str] = []
        for ev in events:
            parts.append(f"User: {ev.input_text}")
            parts.append(f"AI: {ev.output_text}")
        text = " ".join(parts)
        if len(text) > self.max_chars:
            return text[: self.max_chars] + "..."
        return text


class StubEmbedderLLM(Embedder):
    """
    Embedding Adapter.
    It could call a real embeddings model, but here we'll use the core's BagOfWordsEmbedder as a fallback.
    """

    def __init__(self):
        self._inner = BagOfWordsEmbedder()

    def embed(self, text: str) -> List[float]:
        # Here it could include:
        #   - HTTP call to an embeddings service
        #   - or a call to a local model
        return self._inner.embed(text)
