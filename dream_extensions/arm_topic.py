from datetime import datetime, timedelta
from dream.models import EpisodicUnit

class TopicAwareARM:
    def __init__(self, base_ttl_days=7, max_ttl_days=90):
        self.base = base_ttl_days
        self.max = max_ttl_days
        self.topic_access_map = {}

    def on_topic_access(self, topic: str):
        self.topic_access_map[topic] = self.topic_access_map.get(topic, 0) + 1

    def compute_ttl(self, topic: str):
        visits = self.topic_access_map.get(topic, 0)
        ttl = min(self.max, self.base * (2 ** visits))
        return timedelta(days=ttl)

    def apply(self, eu: EpisodicUnit):
        ttl = self.compute_ttl(eu.topic or "default")
        eu.ttl = datetime.utcnow() + ttl
        return eu
