# Skeleton for PostgreSQL + pgvector
class PgVectorStore:
    def __init__(self, conn):
        self.conn = conn

    def index(self, user_id, eu):
        # TODO: insert embedding + metadata using pgvector column
        pass

    def search(self, user_id, query_text, top_k):
        # TODO: cosine distance query with ORDER BY embedding <-> query_embedding
        return []
