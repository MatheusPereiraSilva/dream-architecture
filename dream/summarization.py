from __future__ import annotations
from typing import List
from .models import MemoryEvent
from .interfaces import Summarizer

class SimpleSummarizer(Summarizer):
    """
    Demo: joins the events and truncates at the limit.
    In production, an LLM goes here.
    """
    def __init__(self, max_chars: int = 600):
        self.max_chars = max_chars

    def summarize(self, events: List[MemoryEvent]) -> str:
        parts: List[str] = []
        for ev in events:
            parts.append(f"User: {ev.input_text}")
            parts.append(f"AI: {ev.output_text}")
        joined = " ".join(parts)
        if len(joined) > self.max_chars:
            return joined[: self.max_chars] + "..."
        return joined
