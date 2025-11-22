import matplotlib.pyplot as plt
import numpy as np

# --- Configuration ---
plt.style.use('default')

# 1. Simulation Parameters
simulation_days = 365
episodes_per_day = 5
avg_episode_size = 1.0  # Arbitrary unit (e.g., 1MB)

# --- Scenario A: Naive Storage (Standard) ---
# Saves everything forever. Linear growth.
storage_naive = np.cumsum([episodes_per_day * avg_episode_size] * simulation_days)

# --- Scenario B: DREAM Architecture (ARM) ---
# Uses Adaptive Retention Mechanism (TTL) + Zipfian Revisit Distribution
storage_dream_daily = []
active_episodes = [] # Stores state of each episode: {'ttl_expiration_day': int, 'size': float}

# Set random seed for reproducibility
np.random.seed(42)

for current_day in range(1, simulation_days + 1):
    # A. Create new episodes for today
    for _ in range(episodes_per_day):
        # New episodes start with a short TTL (e.g., 7 days from now)
        active_episodes.append({'ttl_expiration_day': current_day + 7, 'size': avg_episode_size})

    # B. Simulate User Revisits (The "Relevance" Factor)
    # In real life, users revisit a small fraction of memories according to a Power Law
    if len(active_episodes) > 0:
        # Number of revisits today scales slightly with memory size but is limited
        num_revisits = int(np.log1p(len(active_episodes)) * 2)

        # Pick random episodes to revisit
        revisit_indices = np.random.choice(len(active_episodes), size=min(num_revisits, len(active_episodes)), replace=False)

        for idx in revisit_indices:
            episode = active_episodes[idx]
            # ARM Logic: Revisit extends TTL.
            # Here we simulate a "Doubling" or extension effect (e.g., add 14 days)
            episode['ttl_expiration_day'] += 14

    # C. Pruning Process (The "Garbage Collection")
    # Remove episodes that have expired (TTL < current_day)
    # This simulates moving them to Cold Storage or Deletion
    active_episodes = [ep for ep in active_episodes if ep['ttl_expiration_day'] >= current_day]

    # Calculate total active storage for this day
    total_active_size = sum(ep['size'] for ep in active_episodes)
    storage_dream_daily.append(total_active_size)

# 2. Plotting the Graph
plt.figure(figsize=(10, 6))
days = np.arange(1, simulation_days + 1)

# Plot Naive Storage (Orange)
plt.plot(days, storage_naive, color='#ff7f0e', linewidth=3, label='Standard Storage (Cumulative)')

# Plot DREAM Storage (Blue)
plt.plot(days, storage_dream_daily, color='#1f77b4', linewidth=3, label='DREAM (Adaptive Retention - ARM)')

# Styling
plt.title('Storage Cost Comparison (Long-Term Memory)', fontsize=14, fontweight='bold')
plt.xlabel('Usage Time (Days)', fontsize=12)
plt.ylabel('Stored Data Volume (Cumulative)', fontsize=12)
plt.grid(True, linestyle='--', alpha=0.6)
plt.legend(fontsize=11)
plt.yticks([]) # Relative units

# Highlight Savings Area
plt.fill_between(days, storage_dream_daily, storage_naive, color='gray', alpha=0.1, label='Storage Savings')
plt.text(simulation_days - 50, storage_naive[-1]*0.6, 'Massive Storage\nSavings', fontsize=10, color='gray', style='italic', ha='right')

plt.tight_layout()

# Save and Show
plt.savefig('storage_cost_savings.png', dpi=300)
plt.show()
print("Graph 2 generated successfully.")