import uuid
from memory.episodic_db import EpisodicDB
from memory.vector_db import VectorDB
from memory.retrieval import RetrievalService
from core.arm import AdaptiveRetention
from core.summarizer import TextSummarizer
from models.episodic_unit import EpisodicUnit

class DreamOrchestrator:
  """
  The main coordinator (Shard). Connects all components.
  """

  def __init__(self):
    # Initialize Components
    self.episodic_db = EpisodicDB()
    self.vector_db = VectorDB()
    self.arm = AdaptiveRetention()
    self.summarizer = TextSummarizer()

    # Inject dependencies into Retrieval Service
    self.retrieval_service = RetrievalService(
      vector_db=self.vector_db,
      episodic_db=self.episodic_db,
      arm=self.arm
    )

  def save_interaction(self, user_id: str, user_text: str, ai_response: str = ""):
    """
    Full Write Flow (Fig 2.1): Summarize -> Vectorize -> Save
    """
    # 1. Generate Summary
    summary = self.summarizer.summarize(user_text, ai_response)

    # 2. Generate Embedding (Mock)
    embedding = self.vector_db.get_mock_embedding()

    # 3. Create Unit & Initialize TTL
    mem_id = str(uuid.uuid4())[:8]
    memory = EpisodicUnit(
      id=mem_id,
      user_id=user_id,
      content=summary,
      embedding=embedding
    )
    memory.ttl_expiration = self.arm.initialize_ttl()

    # 4. Persist
    self.episodic_db.add_memory(memory)
    self.vector_db.add_vector(mem_id, embedding, {"user_id": user_id})

    print(f"[ORCH] ✅ Memory saved: '{summary}' (ID: {mem_id})")

  def retrieve_context(self, user_id: str, query_text: str):
    """
    Delegates to RetrievalService (Fig 1)
    """
    print(f"\n[ORCH] 🔍 Requesting context for: '{query_text}'...")

    # 1. Vectorize Query
    query_vec = self.vector_db.get_mock_embedding()

    # 2. Delegate to Service
    contexts = self.retrieval_service.search_memories(user_id, query_vec)

    return contexts