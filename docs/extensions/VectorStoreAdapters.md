# Vector Store Adapters — Comparison & Design Notes

This document explains how each supported Vector Store behaves, what use-cases it fits best, and why DREAM remains fully technology-agnostic regardless of the storage backend.

---

## The adapters covered here:

- PostgreSQL + pgvector  
- Qdrant  
- Pinecone 
- (and Cassandra, already documented)
---

## **🔥 1. PostgreSQL + pgvector**
### **Summary**.  
pgvector is a PostgreSQL extension that adds native vector operations (cosine, L2, inner product) to a relational DB.
### **Strengths**
- Relational + vector operations in one place  
- Easy to maintain 
- Works extremely well for small to medium memory stores
- Transactions, RLS, schemas → excellent for per-user isolation
- Perfect for teams that already use PostgreSQL
### **Limitations**
- Not ideal for millions of vectors (index can become large) 
- ANN (Approximate Nearest Neighbor) is available, but slower than Qdrant/Pinecone
- Horizontal scalability requires sharding
### **Fit for DREAM**
Excellent for:
- Local deployments 
- Internal systems 
- Per-user isolated memories
- Prototype / benchmarking

---

## **🚀 2. Qdrant**
### **Summary**.  
Qdrant is an open-source, high-performance vector database designed specifically for ANN search.
### **Strengths**
- Blazing fast ANN (HNSW) 
- Native payload filters (perfect for user_id isolation) 
- Great for large-scale vector storage
- Actively maintained, open-source
- Deployable anywhere (local, Docker, cloud, k8s)
### **Limitations**
- Requires maintaining an additional infrastructure 
- More moving parts than pgvector
- Needs monitoring for memory/collection size
### **Fit for DREAM**
Perfect for:
- Large-scale episodic memory 
- High request-per-second workloads 
- Heavy retrieval use-cases
- Agentic systems with long-term context memory

If you want to showcase that DREAM scales horizontally, Qdrant is the best example.

---

## **☁️ 3. Pinecone**
### **Summary**.  
Pinecone is a fully managed vector service, focused on production and global scalability.
### **Strengths**
- Zero ops (no server management) 
- High-speed ANN 
- Multi-region, enterprise-grade
- Automatic replication & backups
- Extremely simple to integrate
### **Limitations**
- Proprietary
- Not ideal for offline/local experiments
- Costs can become high for large workloads
- Requires internet access
### **Fit for DREAM**
Ideal for:
- Production agents 
- SaaS platforms 
- Distributed memory services
- Teams that want scalability without infra

Great for showing that DREAM is compatible with enterprise-grade vector services.

---

## **🧩 4. Cassandra (from earlier)**
### **Summary**.  
Cassandra is a distributed, linearly scalable NoSQL database. Frequently used for large, write-heavy workloads.
### **Strengths**
- Horizontal scalability
- High availability 
- Fault tolerance
- Massive write throughput
- Good for storing metadata at extreme scale
### **Limitations**
- No native vector support (requires companion ANN index or external search layer)
- More complex operational profile
- Better suited for user metadata + external vector index
### **Fit for DREAM**
Useful when:
- You store huge amounts of episodic metadata 
- You integrate an external ANN search engine
- You need consistency + availability at scale

---

## 🏗 How DREAM Stays Technology-Agnostic
All adapters implement the same minimal interface:

```Python
class VectorStore:
    def index(self, user_id: str, eu: EpisodicUnit): ...
    def search(self, user_id: str, query_text: str, top_k: int): ...

```
Because of this:
- The core (`dream/`) never depends on any specific vector database
- Every storage technology is a plug-and-play module
- Switching from pgvector → Qdrant → Pinecone → Cassandra requires zero changes in the architecture
- DREAM remains a pure design pattern, not a technology stack

---

## 📊 Recommended Use Cases Table

| Store | Scale | Speed | Infra Needed | Filtering | Best Use Case |
|---|---|---|---|---|---|
| pgvector | Small/Medium | Moderate | None (built-in) | SQL native | Local, simple production |
| Qdrant | Medium/Large | Very fast | Docker/k8s | Strong | Agentic AI, heavy RAG |
| Pinecone | Medium/Large | Extremely fast | None (managed cloud) | Strong | Enterprise apps |
| Cassandra | Huge | Varies | Complex cluster | Weak (needs extra layer) | Metadata + distributed memory |

---
