import time


class TTLCache:
    def __init__(self, ttl_seconds: int):
        self.ttl = ttl_seconds
        self.data: dict = {}

    def get(self, key):
        item = self.data.get(key)
        if not item:
            return None

        value, timestamp = item
        if time.time() - timestamp > self.ttl:
            del self.data[key]
            return None

        return value

    def set(self, key, value):
        self.data[key] = (value, time.time())
