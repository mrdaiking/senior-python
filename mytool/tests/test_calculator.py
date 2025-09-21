import pytest

from mytool.calculator import Calculator


class TestCalculator:
    def setup_method(self) -> None:
        self.calc = Calculator()

    def test_add(self) -> None:
        assert self.calc.add(2, 3) == 5
        assert self.calc.add(-1, 1) == 0

    def test_subtract(self) -> None:
        assert self.calc.subtract(5, 3) == 2

    def test_multiply(self) -> None:
        assert self.calc.multiply(3, 4) == 12

    def test_divide(self) -> None:
        assert self.calc.divide(6, 2) == 3.0
        with pytest.raises(ValueError):
            self.calc.divide(1, 0)

    def test_history(self) -> None:
        self.calc.add(2, 3)
        self.calc.multiply(4, 5)
        history = self.calc.get_history()
        assert len(history) == 2
        assert "2 + 3 = 5" in history
        assert "4 * 5 = 20" in history

    def test_clear_history(self) -> None:
        self.calc.add(1, 1)
        assert len(self.calc.get_history()) == 1
        self.calc.clear_history()
        assert len(self.calc.get_history()) == 0
