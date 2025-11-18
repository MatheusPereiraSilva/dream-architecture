# Main file to run the hybrid architecture simulation.
# Instructions:
# 1. Save this file, 'infra_mocks.py', and 'dream_orchestrator.py' in the same folder.
# 2. Run in your terminal: python main.py

# We import from 'infra_mocks.py' which I created in a previous step
from infra_mocks import EpisodicMemoryDB, VectorDB, FrontendClient, SupermemoryAPIClient
from dream_orchestrator import DREAM_OrchestratorShard

# --- 1. Initial Setup (Dependency Injection) ---
print("="*40)
print("INITIALIZING DREAM HYBRID SYSTEM...")
print("="*40)

# Instantiate infrastructure services (mocks)
db = EpisodicMemoryDB()
vdb = VectorDB()
frontend = FrontendClient()

# Instantiate DREAM's "brain" (Orchestrator Shard)
# Note that services are injected into it.
dream_shard = DREAM_OrchestratorShard(db, vdb, frontend)

# Instantiate the Supermemory client and connect it to the Orchestrator's DaaS API
supermemory_client = SupermemoryAPIClient(dream_shard)

# --- 2. PREPARATION: Save a normal DREAM memory ---
print("\n" + "="*40)
print("Preparation Scenario: Saving an initial memory (Ep_001)...")
# (Simulating a prior user opt-in for this memory)
dream_shard.save_new_episode(
    user_id="user_123",
    summary="My initial conversation about the DREAM architecture.",
    embedding="emb_of_dream_arch",
    topic="DREAM",
    source="dream" # Source is DREAM itself
)
# (Let's assume the generated ID was 'ep_001' for logging purposes)

# --- 3. DEMONSTRATION OF HYBRID FLOWS ---

# 3.1 HYBRID FLOW (Pattern 1: PULL)
# Supermemory reads from DREAM to get context, BUT DOES NOT TRIGGER ARM.
episodes = supermemory_client.get_dream_context(
    user_id="user_123",
    query_text="dream arch"
)
# (Note that the logs will NOT show "UPDATE (ARM)")
print(f"[main.py] Supermemory retrieved {len(episodes)} EUs from DREAM.")


# 3.2 HYBRID FLOW (Pattern 2: PUSH)
# Supermemory suggests a memory. DREAM forces Opt-In.
supermemory_client.suggest_memory_to_dream(
    user_id="user_123",
    memory_data={
        "summary": "The user connected Supermemory to Google Drive.",
        "topic": "Integrations"
    }
)
# (Note that the logs will show the Frontend being called and the memory (e..g, 'ep_002') being saved with visits=0)


# 3.3 NORMAL FLOW (ARM ACTIVE)
# The user now talks to the LLM. The LLM fetches context.
# DREAM retrieves the memory AND TRIGGERS ARM.
dream_shard.handle_user_query(
    user_id="user_123",
    query_text="Remind me about my initial conversation."
)
# (Note that the logs will NOW SHOW: "UPDATE (ARM): Ep_001 now has 1 visits.")

# 3.4 ARM VERIFICATION
# If the user asks again, the visit counter should go to 2
dream_shard.handle_user_query(
    user_id="user_123",
    query_text="Tell me more about the DREAM architecture."
)
# (Note that the logs will show "UPDATE (ARM): Ep_001 now has 2 visits." and the TTL will be longer)

print("\n" + "="*40)
print("Simulation complete.")
print("="*40)