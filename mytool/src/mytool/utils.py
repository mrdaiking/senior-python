# Bạn có thể thêm các hàm tiện ích khác tại đây và test tương ứng sau
from typing import Iterator


def fibonacci(n: int) -> Iterator[int]:
    """Sinh dãy Fibonacci n phần tử."""
    a, b = 0, 1
    for _ in range(n):
        yield a
        a, b = b, a + b
