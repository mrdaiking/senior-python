import pytest

from mytool.text_processor import TextProcessor


class TestTextProcessor:
    def setup_method(self) -> None:
        self.processor = TextProcessor()

    def test_word_count(self) -> None:
        text = "hello world hello"
        result = self.processor.word_count(text)
        assert result["hello"] == 2
        assert result["world"] == 1
        assert len(result) == 2

    def test_word_count_case_insensitive(self) -> None:
        processor = TextProcessor(case_sensitive=False)
        text = "Hello HELLO hello"
        result = processor.word_count(text)
        assert result["hello"] == 3
        assert len(result) == 1

    def test_find_longest_word(self) -> None:
        text = "short medium verylongword tiny"
        result = self.processor.find_longest_word(text)
        assert result == "verylongword"

    def test_find_longest_word_empty(self) -> None:
        result = self.processor.find_longest_word("")
        assert result is None

    def test_reverse_words(self) -> None:
        text = "hello world python"
        result = self.processor.reverse_words(text)
        assert result == "python world hello"
