# Skeleton for Qdrant Vector Store
class QdrantVectorStore:
    def __init__(self, client):
        self.client = client

    def index(self, user_id, eu):
        # TODO: client.upsert with payload (user_id, topic, summary)
        pass

    def search(self, user_id, query_text, top_k):
        # TODO: client.search with filter on user_id
        return []
