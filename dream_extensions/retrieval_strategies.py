from typing import List
from dream.models import EpisodicUnit

class RetrievalStrategy:
    def retrieve(self, user_id: str, query_text: str, top_k: int) -> List[EpisodicUnit]:
        raise NotImplementedError

class SemanticRetrieval(RetrievalStrategy):
    def __init__(self, vector_store):
        self.vs = vector_store

    def retrieve(self, user_id, query_text, top_k):
        return self.vs.search(user_id, query_text, top_k)

class HybridRetrieval(RetrievalStrategy):
    def __init__(self, vector_store, bm25):
        self.vs = vector_store
        self.bm25 = bm25

    def retrieve(self, user_id, query_text, top_k):
        lexical = set(self.bm25.search(user_id, query_text, top_k))
        semantic = set(self.vs.search(user_id, query_text, top_k))
        combined = list(lexical.union(semantic))
        return combined[:top_k]

class RerankingRetrieval(RetrievalStrategy):
    def __init__(self, vector_store, reranker):
        self.vs = vector_store
        self.reranker = reranker

    def retrieve(self, user_id, query_text, top_k):
        cand = self.vs.search(user_id, query_text, top_k*3)
        reranked = self.reranker.rerank(query_text, cand)
        return reranked[:top_k]
