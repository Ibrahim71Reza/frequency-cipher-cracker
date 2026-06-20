from collections import Counter
from .text import clean_text, ALPHABET


def letter_frequency(text: str) -> dict:
    cleaned = clean_text(text)
    total = len(cleaned)

    if total == 0:
        return {letter: 0.0 for letter in ALPHABET}

    counts = Counter(cleaned)

    return {
        letter: round((counts.get(letter, 0) / total) * 100, 2)
        for letter in ALPHABET
    }


def ngram_frequency(text: str, n: int = 2, top: int = 10) -> list:
    cleaned = clean_text(text)

    if len(cleaned) < n:
        return []

    ngrams = [cleaned[i:i+n] for i in range(len(cleaned) - n + 1)]
    counts = Counter(ngrams)

    return counts.most_common(top)


def index_of_coincidence(text: str) -> float:
    cleaned = clean_text(text)
    n = len(cleaned)

    if n <= 1:
        return 0.0

    counts = Counter(cleaned)
    ic = sum(count * (count - 1) for count in counts.values()) / (n * (n - 1))

    return round(ic, 4)
