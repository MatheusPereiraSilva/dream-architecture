import time
from models.episodic_unit import EpisodicUnit

class AdaptiveRetention:
  """
  Manages the lifecycle of memories (Adaptive Retention Mechanism - ARM).
  Implements the 'Tiered Storage' logic defined in DREAM v2.0.
  """

  def __init__(self, base_ttl_days=7):
    self.base_ttl_days = base_ttl_days
    self.max_ttl_days = 365

  def initialize_ttl(self) -> float:
    """Calculates the initial expiration timestamp (e.g., 7 days from now)."""
    return time.time() + (self.base_ttl_days * 86400)

  def process_revisit(self, memory: EpisodicUnit):
    """
    Core ARM Logic:
    1. Increments visit count.
    2. Doubles (expands) the TTL based on engagement.
    3. Restores from 'DORMANT' to 'ACTIVE' tier if necessary.
    """
    memory.visits += 1

    # Formula: TTL = Base * (2 ^ visits)
    # Ex: Visit 0 -> +7 days
    #     Visit 1 -> +14 days
    #     Visit 2 -> +28 days
    days_to_add = self.base_ttl_days * (2 ** memory.visits)
    days_to_add = min(days_to_add, self.max_ttl_days)

    # Update expiration timestamp
    memory.ttl_expiration = time.time() + (days_to_add * 86400)

    # If it was in Cold Storage, move it back to Active Memory
    if memory.status == "DORMANT":
      memory.status = "ACTIVE"
      print(f"   [ARM] 🔥 Memory '{memory.id}' reactivated from Cold Storage!")
    else:
      print(f"   [ARM] 🔄 TTL renewed: +{days_to_add} days.")

  def check_lifecycle(self, memory: EpisodicUnit):
    """
    Runs periodically or upon access. Decides if memory should move to Cold Storage.
    """
    if memory.status == "ACTIVE" and memory.is_expired():
      memory.status = "DORMANT"  # Soft Delete implementation
      print(f"   [ARM] ❄️ TTL expired. Memory '{memory.id}' moved to Cold Storage.")