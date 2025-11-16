# Topic-Aware ARM (Adaptive Retention Mechanism)

This extension improves DREAM by adjusting TTL based on *topic-level activity* rather than only per-EU usage.

## Motivation
The original ARM uses visits count per episodic unit.  
However, some feedback suggests that topics should decay as a group.

## Formula (proposed)

```
TTL_days = base_ttl * 2^(topic_visits)
```

Where:
- `topic_visits` = total retrieval count for all EUs of the same topic
- `base_ttl` = default (e.g., 7 days)

## Behavior
- If a topic is not accessed for a while, all EUs inside it lose TTL.
- Prevents “ghost relevance” where a relevant EU dies only because its specific ID wasn’t accessed recently.

