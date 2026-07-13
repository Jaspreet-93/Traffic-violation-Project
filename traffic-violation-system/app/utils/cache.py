import time

class SimpleCache:
    def __init__(self):
        self._cache = {}

    def get(self, key):
        if key in self._cache:
            val, expiry = self._cache[key]
            if expiry is None or expiry > time.time():
                return val
            else:
                del self._cache[key]
        return None

    def set(self, key, value, ttl=None):
        # ttl in seconds
        expiry = time.time() + ttl if ttl else None
        self._cache[key] = (value, expiry)

    def clear(self):
        self._cache.clear()

global_cache = SimpleCache()
