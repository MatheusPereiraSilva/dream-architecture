from __future__ import annotations
from typing import Dict, List
import math

def cosine_similarity(a: List[float], b: List[float]) -> float:
    if not a or not b:
        return 0.0
    size = min(len(a), len(b))
    num = sum(a[i] * b[i] for i in range(size))
    den_a = math.sqrt(sum(a[i] * a[i] for i in range(size))) or 1.0
    den_b = math.sqrt(sum(b[i] * b[i] for i in range(size))) or 1.0
    return num / (den_a * den_b)


class BagOfWordsEmbedder:
    """
    Demo embedding to test the DREAM pattern.
    In production: replace with OpenAI, HF, etc.
    """
    def __init__(self):
        self._vocab: Dict[str, int] = {}

    def _tokenize(self, text: str) -> List[str]:
        return [t.lower() for t in text.split() if t.strip()]

    def _ensure_vocab(self, tokens: List[str]) -> None:
        for tok in tokens:
            if tok not in self._vocab:
                self._vocab[tok] = len(self._vocab)

    def embed(self, text: str) -> List[float]:
        tokens = self._tokenize(text)
        self._ensure_vocab(tokens)
        vec = [0.0] * len(self._vocab)
        for tok in tokens:
            idx = self._vocab[tok]
            vec[idx] += 1.0
        norm = math.sqrt(sum(v * v for v in vec)) or 1.0
        return [v / norm for v in vec]
