from __future__ import annotations
from datetime import datetime, timedelta
from .models import EpisodicUnit

class AdaptiveRetentionMechanism:
    """
    TTL_days = min(TTL_MAX_DAYS, 7 * 2^visits)
    """
    def __init__(self, ttl_max_days: int = 365, base_days: int = 7):
        self.ttl_max_days = ttl_max_days
        self.base_days = base_days

    def compute_ttl_days(self, visits: int) -> int:
        ttl = self.base_days * (2 ** visits)
        return min(ttl, self.ttl_max_days)

    def next_expiration(self, now: datetime, visits: int) -> datetime:
        days = self.compute_ttl_days(visits)
        return now + timedelta(days=days)

    def initialize_eu(self, eu: EpisodicUnit, now: datetime) -> EpisodicUnit:
        eu.visits = 0
        eu.ttl = self.next_expiration(now, eu.visits)
        return eu

    def on_reuse(self, eu: EpisodicUnit, now: datetime) -> EpisodicUnit:
        eu.visits += 1
        eu.ttl = self.next_expiration(now, eu.visits)
        return eu
