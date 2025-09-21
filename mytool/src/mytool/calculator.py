from typing import Union

Number = Union[int, float]


class Calculator:
    """A simple calculator with type hints and history."""

    def __init__(self) -> None:
        self.history: list[str] = []

    def add(self, a: Number, b: Number) -> Number:
        result = a + b
        self.history.append(f"{a} + {b} = {result}")
        return result

    def subtract(self, a: Number, b: Number) -> Number:
        result = a - b
        self.history.append(f"{a} - {b} = {result}")
        return result

    def multiply(self, a: Number, b: Number) -> Number:
        result = a * b
        self.history.append(f"{a} * {b} = {result}")
        return result

    def divide(self, a: Number, b: Number) -> float:
        if b == 0:
            raise ValueError("Cannot divide by zero")
        result = a / b
        self.history.append(f"{a} / {b} = {result}")
        return result

    def get_history(self) -> list[str]:
        return self.history.copy()

    def clear_history(self) -> None:
        self.history.clear()
