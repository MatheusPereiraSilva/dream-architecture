import matplotlib.pyplot as plt
import numpy as np

# --- Configuration ---
plt.style.use('default')

# 1. Simulation Data Setup
# Simulating conversation history growing from 1k to 100k tokens
history_tokens = np.arange(1000, 100001, 1000)

# Architecture Settings
standard_llm_window = 128000  # Example: GPT-4 Turbo (128k context)
dream_fixed_window = 4096     # DREAM maintains a fixed, short context window

# Cost Functions
def standard_transformer_cost(history_size):
    """
    Standard Transformers have quadratic attention cost O(n^2).
    Cost grows exponentially as history fills the context window.
    """
    active_context = np.minimum(history_size, standard_llm_window)
    # Normalizing to an arbitrary relative scale (FLOPs estimate)
    return (active_context ** 2) / 1e9

def dream_architecture_cost(history_size):
    """
    DREAM uses a fixed window O(c^2) + Vector Retrieval (Linear/Log).
    Cost remains stable regardless of total history size.
    """
    # Fixed inference cost (small window)
    inference_cost = (dream_fixed_window ** 2)

    # Marginal cost of vector search (Retrieval is extremely cheap compared to attention)
    retrieval_cost = history_size * 100

    return (inference_cost + retrieval_cost) / 1e9

# Calculate Costs
costs_standard = standard_transformer_cost(history_tokens)
costs_dream = [dream_architecture_cost(h) for h in history_tokens]

# 2. Plotting the Graph
plt.figure(figsize=(10, 6))

# Plot Standard Architecture (Red)
plt.plot(history_tokens, costs_standard, color='#d62728', linewidth=3, label='Standard Architecture (Infinite Window)')

# Plot DREAM Architecture (Green)
plt.plot(history_tokens, costs_dream, color='#2ca02c', linewidth=3, label='DREAM Architecture (Fixed Window + RAG)')

# Styling
plt.title('Computational Cost Comparison (Energy Estimate)', fontsize=14, fontweight='bold')
plt.xlabel('Conversation History Size (Tokens)', fontsize=12)
plt.ylabel('Relative Computational Cost (FLOPs)', fontsize=12)
plt.grid(True, linestyle='--', alpha=0.6)
plt.legend(fontsize=11)
plt.yticks([]) # Remove specific units to focus on the trend

# Annotations
plt.text(60000, max(costs_standard)*0.6, 'Exponential Growth\n(Quadratic Cost)', color='#d62728', fontsize=10, ha='center')
plt.text(60000, max(costs_dream)*2.5, 'Stable & Low Cost', color='#2ca02c', fontsize=10, ha='center')

plt.tight_layout()

# Save and Show
plt.savefig('computational_cost_energy.png', dpi=300)
plt.show()
print("Graph 1 generated successfully.")