from dream import (
    DreamOrchestrator,
    SimpleSummarizer,
    BagOfWordsEmbedder,
    InMemoryVectorStore,
)

def main():
    summarizer = SimpleSummarizer(max_chars=400)
    embedder = BagOfWordsEmbedder()
    store = InMemoryVectorStore()
    orchestrator = DreamOrchestrator(
        summarizer=summarizer,
        embedder=embedder,
        vector_store=store,
    )

    user_id = "user_123"
    orchestrator.configure_user(user_id, opted_in=True)

    # 1) Interactions
    orchestrator.record_interaction(
        user_id,
        "Hi, I really like tabletop RPGs, especially D&D.",
        "Cool! I'll remember that to suggest RPG and D&D stuff to you.",
    )
    orchestrator.record_interaction(
        user_id,
        "I also study software architecture and AI.",
        "Great, that opens up room for deeper technical discussions.",
    )
    orchestrator.record_interaction(
        user_id,
        "I'm creating a Discord bot to help with RPG sessions.",
        "Perfect, you can integrate character sheets, rolls, and even AI for NPCs.",
    )

    if orchestrator.should_propose_episode(user_id):
        proposal = orchestrator.build_episode_proposal(
            user_id=user_id,
            topic="RPG + Architecture + Discord Bot",
        )
        if proposal:
            eu = orchestrator.confirm_episode(
                proposal,
                user_confirmed=True,
                importance_score=0.9,
            )
            print("Episode saved:")
            print("  ID:", eu.episode_id)
            print("  Topic:", eu.topic)
            print("  TTL:", eu.ttl)
            print("  Summary:", eu.summary)

    print("\n--- New session: retrieving context ---")
    query = "I want to continue that Discord bot project for RPGs."
    eus = orchestrator.retrieve_context(user_id, query_text=query, top_k=3)

    for eu in eus:
        print("\nRelevant EU:")
        print("  ID:", eu.episode_id)
        print("  Visits:", eu.visits)
        print("  TTL:", eu.ttl)
        print("  Summary:", eu.summary)

    orchestrator.prune_expired()


if __name__ == "__main__":
    main()
