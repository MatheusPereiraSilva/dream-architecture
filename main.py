import time
from core import DreamOrchestrator

def main():
  dream = DreamOrchestrator()
  user_id = "matheus_user"

  print("=== 🧠 STARTING DREAM SYSTEM v2.0 (SIMULATION) ===\n")

  # 1. Learning Phase (User teaches something)
  print("--- 1. Learning Phase ---")
  dream.save_interaction(user_id, "User enjoys programming in Python.")
  dream.save_interaction(user_id, "The current project is called DREAM.")
  time.sleep(1)

  # 2. Retrieval Phase (User asks something)
  # Since we use random embeddings, it will 'find' whatever we saved
  # just to demonstrate the code flow.
  print("\n--- 2. Retrieval & ARM Update Phase ---")
  contexts = dream.retrieve_context(user_id, "What do I like to program?")

  print(f"\n📝 Context Retrieved for LLM: {contexts}")

  # 3. Time Passage Simulation (Hack to force expiration)
  print("\n--- 3. Simulating Time Passage (Soft Delete Test) ---")
  # We will pick a memory and force its expiration manually
  all_memories = dream.episodic_db.list_all()
  if all_memories:
    test_memory = all_memories[0]
    print(f"   -> Forcing expiration on memory: '{test_memory.content}'")
    test_memory.ttl_expiration = time.time() - 1000  # Expired in the past

    # Now we try to access it again. The system must detect it expired,
    # mark it as DORMANT, but then reactivate it because we requested it.
    dream.retrieve_context(user_id, "Test question to trigger reactivation")


if __name__ == "__main__":
  main()