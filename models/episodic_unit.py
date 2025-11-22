import time
from dataclasses import dataclass, field
from typing import List

@dataclass
class EpisodicUnit:
  """
  Represents a single episodic memory unit within the DREAM system.
  """
  id: str
  user_id: str
  content: str  # The textual summary
  embedding: List[float]  # Vector for semantic search

  # Lifecycle Metadata (ARM)
  created_at: float = field(default_factory=time.time)
  visits: int = 0
  ttl_expiration: float = 0.0
  status: str = "ACTIVE"  # Values: ACTIVE, DORMANT (Cold Storage), DELETED

  def is_expired(self) -> bool:
    """Checks if the Time-To-Live (TTL) has expired."""
    return time.time() > self.ttl_expiration