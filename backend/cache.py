"""Caching layer for performance"""
from typing import Optional, Any
from datetime import timedelta

class CacheManager:
    """Manages caching for frequently accessed data"""

    def __init__(self):
        self.cache: dict = {}

    def get(self, key: str) -> Optional[Any]:
        """Get value from cache"""
        return self.cache.get(key)

    def set(self, key: str, value: Any, ttl: Optional[timedelta] = None):
        """Set value in cache"""
        self.cache[key] = value

    def invalidate(self, pattern: str):
        """Invalidate cache entries matching pattern"""
        keys_to_delete = [k for k in self.cache.keys() if pattern in k]
        for key in keys_to_delete:
            del self.cache[key]

cache_manager = CacheManager()
