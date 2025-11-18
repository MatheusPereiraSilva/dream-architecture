# Contains mock classes for infrastructure services
# and external APIs, such as databases and the Supermemory client.

class EpisodicMemoryDB:
  """Mock for your main database (e.g., Cassandra, DynamoDB) """

  def __init__(self):
    self._db = {}
    print(" EpisodicMemoryDB (Cassandra/DynamoDB) initialized.")

  def insert_episode(self, episode_data):
    ep_id = episode_data['episode_id']
    print(f" INSERT: Ep_{ep_id} (TTL: {episode_data['ttl']})")
    self._db[ep_id] = episode_data

  def get_episodes_by_ids(self, user_id, ids):
    print(f" GET: Fetching {len(ids)} episodes for {user_id}")
    return [self._db[id] for id in ids if id in self._db and self._db[id]['user_id'] == user_id]

  def update_episode(self, episode_data):
    # This is the crucial call for ARM
    ep_id = episode_data['episode_id']
    print(f" UPDATE (ARM): Ep_{ep_id} now has {episode_data['visits']} visits. New TTL: {episode_data['ttl']}")
    self._db[ep_id] = episode_data


class VectorDB:
  """Mock for your vector database (e.g., FAISS, Pinecone) """

  def __init__(self):
    self._index = {}  # Simulates a vector index
    print(" VectorDB (Pinecone/FAISS) initialized.")

  def search(self, user_id, query_embedding, top_k):
    print(f" SEARCH: Searching for {top_k} memories for {user_id}...")
    # Simulates locating relevant memories
    if "supermemory" in query_embedding:
      return ["ep_002"]  # Returns the episode ID saved by Supermemory
    return ["ep_001"]  # Returns a normal episode ID

  def insert(self, user_id, episode_id, embedding):
    print(f" INSERT: Indexing Ep_{episode_id} for {user_id}")
    self._index[episode_id] = embedding  # Simulates insertion


class FrontendClient:
  """Mock for the user interface that handles Opt-In """

  def __init__(self):
    print(" FrontendClient initialized.")

  def ask_user_for_opt_in(self, user_id, summary_text):
    """Simulates asking the user for opt-in """
    print(f"\n[Frontend] PROMPT: User {user_id}, Supermemory suggested saving:")
    print(f"   '{summary_text}'")
    print(f"   Do you want to save this memory? (y/n)")
    # In a real application, this would be an asynchronous API call.
    # For this example, let's simulate the user saying 'yes'.
    response = 'y'
    print(f"[Frontend] RESPONSE: User said '{response}'")
    return response == 'y'


class SupermemoryAPIClient:
  """
  Mock for the Supermemory API client.
  IMPORTANT: It does not connect to DREAM's DB, but to the Orchestrator.
  """

  def __init__(self, dream_orchestrator):
    # Receives the orchestrator instance to communicate with the DaaS API
    self.dream_orchestrator = dream_orchestrator
    print(" Supermemory Client initialized. Connected to DaaS Orchestrator.")

  def get_dream_context(self, user_id, query_text):
    print("\n" + "=" * 40)
    print(f" PULL FLOW: Fetching episodic context from DREAM for: '{query_text}'")

    # Calls the "read" DaaS API on the orchestrator
    episodes = self.dream_orchestrator.daas_retrieve_episodes(
      user_id=user_id,
      query_text=query_text
    )
    print(f" PULL context received from DREAM: {len(episodes)} episodes.")
    return episodes

  def suggest_memory_to_dream(self, user_id, memory_data):
    print("\n" + "=" * 40)
    print(f" PUSH FLOW: Suggesting new memory for DREAM to save:")
    print(f"   '{memory_data['summary']}'")

    # Calls the "write" DaaS API on the orchestrator
    status = self.dream_orchestrator.daas_submit_for_retention(
      user_id=user_id,
      payload=memory_data
    )
    print(f" PUSH Status: {status}")