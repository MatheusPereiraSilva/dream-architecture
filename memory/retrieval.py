from typing import List
from memory.vector_db import VectorDB
from memory.episodic_db import EpisodicDB
from core.arm import AdaptiveRetention

class RetrievalService:
  """
  Implements the 'Memory Retrieval Service' block from the architecture diagram.
  Orchestrates Vector Search -> Metadata Fetch -> ARM Lifecycle Check.
  """

  def __init__(self, vector_db: VectorDB, episodic_db: EpisodicDB, arm: AdaptiveRetention):
    self.vector_db = vector_db
    self.episodic_db = episodic_db
    self.arm = arm

  def search_memories(self, user_id: str, query_embedding: List[float], n_results=3) -> List[str]:
    """
    Executes the full retrieval pipeline.
    """
    # 1. Semantic Search in Vector DB
    results = self.vector_db.search(query_embedding, n_results)

    found_contents = []

    if results['ids']:
      # The structure of results is [[id1, id2...]]
      ids_list = results['ids'][0]

      for mem_id in ids_list:
        # 2. Fetch Metadata from Episodic DB
        memory = self.episodic_db.get_memory(mem_id)
        if not memory:
          continue

        # 3. Lifecycle Check (Soft Delete Logic)
        self.arm.check_lifecycle(memory)

        if memory.status == "DORMANT":
          print(f"   [RETRIEVAL] ⚠️ Memory '{memory.id}' is in Cold Storage. Reactivating for usage...")

        # 4. Update ARM (Revisit Logic)
        # Since we retrieved it, it counts as a visit!
        self.arm.process_revisit(memory)

        # Persist the updates (new TTL/visits)
        self.episodic_db.update_memory(memory)

        found_contents.append(memory.content)

    return found_contents