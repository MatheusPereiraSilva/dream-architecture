class EpisodicDB:
  """
  Simulates the metadata storage (Key-Value Store).
  In production, this would be SQLite, PostgreSQL, or Cassandra.
  """

  def __init__(self):
    self.storage = {}  # In-memory dictionary for demonstration

  def add_memory(self, memory):
    self.storage[memory.id] = memory

  def get_memory(self, memory_id):
    return self.storage.get(memory_id)

  def update_memory(self, memory):
    self.storage[memory.id] = memory

  def list_all(self):
    return list(self.storage.values())