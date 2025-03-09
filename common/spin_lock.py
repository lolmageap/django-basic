import time
import uuid
from functools import wraps

from django.core.cache import caches


class SpinLock:
    def __init__(
            self,
            key: str,
            timeout: int = 5,
            retry_interval: float = 0.1,
            cache_alias: str = "default",
    ):
        self.key = key
        self.timeout = timeout
        self.retry_interval = retry_interval
        self.cache = caches[cache_alias]
        self.lock_value = str(uuid.uuid4())

    def acquire(self) -> bool:
        expire_at = time.time() + self.timeout

        while time.time() < expire_at:
            if self.cache.add(self.key, self.lock_value, self.timeout):
                return True
            time.sleep(self.retry_interval)

        return False

    def release(self):
        if self.cache.get(self.key) == self.lock_value:
            self.cache.delete(self.key)

    def __enter__(self):
        if not self.acquire():
            raise TimeoutError("Failed to acquire lock")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.release()

    def __call__(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            with self:
                return func(*args, **kwargs)

        return wrapper
