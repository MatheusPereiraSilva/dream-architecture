# Extended Retrieval Strategies

This file documents additional retrieval mechanisms beyond simple vector similarity.

## 1. Hybrid Retrieval (BM25 + Embeddings)
- Retrieves documents using BM25 lexical search.
- Re-ranks intersection using embedding cosine similarity.

## 2. Reranking Strategy
- First retrieve top-N by embedding.
- Then send candidate pairs to a `cross-encoder` for reranking.

## 3. Graph-Based Retrieval (GraphRAG-like)
- Builds topic nodes.
- Connects EUs by co-occurrence.
- Retrieves subgraphs relevant to query.

