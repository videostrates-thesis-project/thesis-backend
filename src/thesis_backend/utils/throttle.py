import time
from functools import wraps
from typing import NamedTuple


class CacheEntry(NamedTuple):
    value: any
    expiration_time: float


def make_key(args: tuple, kwargs: dict) -> str:
    # args include self, so it is unique for each instance of the class
    return str(args) + str(kwargs)


def throttle(interval: int) -> callable:
    """
    Decorator throttling the function calls. It caches the result of the function for a specified interval.
    Intended to throttle the number of requests to the Azure Video Indexer API.
    """

    def decorator(func: callable) -> callable:
        cache: dict[str, CacheEntry] = {}

        @wraps(func)
        def wrapper(*args, **kwargs):
            nonlocal cache
            key = make_key(args, kwargs)
            cached_value = cache.get(key)
            if cached_value and time.time() < cached_value.expiration_time:
                return cached_value.value
            result = func(*args, **kwargs)
            cache[key] = CacheEntry(result, time.time() + interval)
            return result
        # Expose a method to clear cache - useful for tests, because the key is based on the memory address,
        # which can repeat in different tests, and since the cache is shared between tests, it can cause weird behaviour
        wrapper.cache_reset = lambda: cache.clear()
        return wrapper

    return decorator
