import time
from functools import wraps

# Function decorator: benchmark

def benchmark(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"[benchmark] {func.__name__} took {end - start:.6f}s")
        return result
    return wrapper

# Class decorator: log_init

def log_init(cls):
    orig_init = cls.__init__
    def __init__(self, *args, **kwargs):
        print(f"[log_init] Creating instance of {cls.__name__}")
        orig_init(self, *args, **kwargs)
    cls.__init__ = __init__
    return cls

# Example usage
if __name__ == "__main__":
    @benchmark
    def slow_add(a, b):
        time.sleep(0.5)
        return a + b

    @log_init
    class User:
        def __init__(self, name):
            self.name = name

    slow_add(2, 3)
    u = User("Alice")
