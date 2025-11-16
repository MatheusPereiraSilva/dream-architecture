# DREAM Architecture
**D.R.E.A.M. — Dynamic Retention Episodic Architecture for Memory**

DREAM is an episodic memory design pattern for AI systems, created to address a core limitation of Large Language Models (LLMs):  
their inability to maintain long-term, relevant, low-noise contextual memory without degrading performance.

📄 **Official Paper:**  
https://doi.org/10.5281/zenodo.17619917

---

## 📌 Overview

DREAM proposes a scalable, adaptive, user‑oriented memory architecture built on four pillars:

### **1. Episodic Units (EUs)**
Compact memory units containing:
- summary  
- embedding vector  
- topic (optional)  
- importance score (optional)  
- visits counter (reuse frequency)  
- ttl (expiration time, managed by ARM)

---

### **2. Opt‑in per Episode**
Every episode is stored **only if explicitly confirmed** (user or system).  
This eliminates:
- noise  
- irrelevant memories  
- vector pollution  
- long‑term drift and hallucination reinforcement  

---

### **3. ARM — Adaptive Retention Mechanism**
Inspired by human memory retention:

```
TTL_days = min(MAX_DAYS, 7 * 2^visits)
```

Meaning:
- Rarely used memories expire quickly  
- Frequently reused memories gain longevity  
- Vector storage stays clean and finite  

---

### **4. Multi‑Orchestrator Sharding**
Horizontal scalability strategy:

```
shard_id = hash(user_id) % N
```

Each user always maps to the same shard → isolation, stability, and efficient distribution.

---

## 🎯 What DREAM Solves

LLMs suffer from:
- context window limitations  
- forgetting over long interactions  
- memory noise accumulation  
- vector databases becoming polluted  
- poor “auto‑RAG” strategies  
- lack of semantic importance differentiation  

DREAM solves these through:
- episodic units  
- TTL based on actual usage  
- explicit memory decisions  
- adaptive retention  
- per‑user isolation  
- lean and clean vector‑based retrieval  

---

## 🏗 Repository Structure

```
dream-architecture/
  dream/                      ← DOMAIN LAYER
    models.py
    interfaces.py
    summarization.py
    embedding.py
    store.py
    arm.py
    orchestrator.py

  app/
    config.py                 ← CONFIG LAYER
    llm_clients.py            ← LLM ADAPTERS
    vector_clients.py         ← VECTOR STORE ADAPTER
    memory_service.py         ← APPLICATION LAYER

    api/                      ← INTERFACE LAYER (FastAPI)
      main.py
      routes_memory.py

  examples/
    simple_demo.py            ← USAGE EXAMPLE
```

---

## 🧠 Domain Layer (Core)

The `dream/` directory contains the pure implementation of the pattern:

- EpisodicUnit  
- MemoryEvent  
- EpisodeProposal  
- AdaptiveRetentionMechanism (ARM)  
- DreamOrchestrator  
- Summarizer / Embedder interfaces  
- In‑memory VectorStore  
- Sharding logic  

This layer has **zero dependency** on external technologies.

---

## ⚙️ Infrastructure (Adapters)

The `app/` layer contains plug‑and‑replace adapters for:
- LLM summarization  
- LLM embeddings  
- Vector store (in‑memory by default, compatible with pgvector, Pinecone, Milvus, Cassandra, etc.)

---

## 🔧 Application Layer (Services)

`MemoryService` contains the true use‑cases:

- record interaction  
- check if an episode should be proposed  
- generate proposals (summary + embedding)  
- confirm or discard episodes  
- retrieve relevant context  
- apply ARM on every reuse  

This is the layer your AI agent or backend would interact with.

---

## 🌐 REST API (FastAPI)

Available endpoints:

### `POST /memory/users/{id}/interactions`
Record interaction into the episodic buffer.

### `POST /memory/users/{id}/episodes/propose`
Generate an episode proposal.

### `POST /memory/users/{id}/episodes/confirm`
Confirm or discard an episode (opt‑in).

### `GET /memory/users/{id}/context?query=...`
Retrieve relevant episodic units (semantic search + ARM).

---

## 🖼 Conceptual Diagram (Text Representation)

```
User Interaction
        ↓
DreamOrchestrator (buffer)
        ↓
EpisodeProposal (summary + embedding)
        ↓  User decision
YES → EpisodicUnit stored
NO  → Discarded
        ↓ (retrieval)
Relevant Episodes
        ↓
ARM.on_reuse → increases visits + extends TTL
```

---

## 🧪 Python Usage Example

```python
from app.memory_service import MemoryService

svc = MemoryService()
user = "user_123"

svc.record_interaction(user, "I like RPG games.", "Nice!")
svc.record_interaction(user, "I study AI.", "Great!")

if svc.should_propose_episode(user):
    prop = svc.build_episode_proposal(user, topic="Interests")
    eu = svc.confirm_episode(prop, user_confirmed=True)

ctx = svc.retrieve_context(user, query_text="AI and RPG")
print(ctx)
```

---

## ⭐ What Makes DREAM Unique

- Saves **only meaningful** memories  
- TTL based on real use  
- User‑centric memory retention  
- Avoids vector database pollution  
- Horizontal scalability via sharding  
- Plug‑and‑play architecture  
- Explicit control over memory creation  
- A new approach to context longevity  
---

“DREAM supports any vector storage backend. Examples provided include pgvector, Qdrant, Pinecone, and Cassandra.
The architecture remains fully independent of underlying technologies.”
---

## 🙌 Contributing

Pull requests are welcome!  
Ideas for new adapters, enhancements to ARM, or improved retrieval strategies are especially appreciated.

---

## 📜 License
Creative Commons Attribution 4.0 International

