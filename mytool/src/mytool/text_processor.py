import re
from typing import Dict, Optional


class TextProcessor:
    """Text processing utilities with type hints."""

    def __init__(self, case_sensitive: bool = True) -> None:
        self.case_sensitive = case_sensitive

    def word_count(self, text: str) -> Dict[str, int]:
        if not self.case_sensitive:
            text = text.lower()
        words = re.findall(r"\b\w+\b", text)
        counts: Dict[str, int] = {}
        for word in words:
            counts[word] = counts.get(word, 0) + 1
        return counts

    def find_longest_word(self, text: str) -> Optional[str]:
        words = re.findall(r"\b\w+\b", text)
        if not words:
            return None
        return max(words, key=len)

    def reverse_words(self, text: str) -> str:
        words = text.split()
        return " ".join(reversed(words))
