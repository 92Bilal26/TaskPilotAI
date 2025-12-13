"""Performance monitoring and optimization"""
import time
from functools import wraps
from typing import Callable

def monitor_performance(func: Callable):
    """Decorator to monitor function performance"""
    @wraps(func)
    async def wrapper(*args, **kwargs):
        start = time.time()
        result = await func(*args, **kwargs)
        duration = time.time() - start
        print(f"{func.__name__} took {duration:.3f}s")
        return result
    return wrapper
