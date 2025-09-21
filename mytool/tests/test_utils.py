from mytool.utils import fibonacci


def test_fibonacci():
    assert list(fibonacci(6)) == [0, 1, 1, 2, 3, 5]
    assert list(fibonacci(0)) == []
    assert list(fibonacci(1)) == [0]
