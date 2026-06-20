from .text import clean_text

ENGLISH_FREQ = {
    "A": 8.12, "B": 1.49, "C": 2.71, "D": 4.32, "E": 12.02,
    "F": 2.30, "G": 2.03, "H": 5.92, "I": 7.31, "J": 0.10,
    "K": 0.69, "L": 3.98, "M": 2.61, "N": 6.95, "O": 7.68,
    "P": 1.82, "Q": 0.11, "R": 6.02, "S": 6.28, "T": 9.10,
    "U": 2.88, "V": 1.11, "W": 2.09, "X": 0.17, "Y": 2.11,
    "Z": 0.07,
}

COMMON_WORDS = [
    "THE", "AND", "THAT", "HAVE", "FOR", "NOT", "WITH", "YOU",
    "THIS", "BUT", "HIS", "FROM", "THEY", "SAY", "HER", "SHE",
    "WILL", "ONE", "ALL", "WOULD", "THERE", "THEIR", "HELLO",
    "WORLD", "TEST", "MESSAGE",
]


def chi_square_score(text: str) -> float:
    """
    Lower score means the text is closer to normal English letter frequency.
    """
    cleaned = clean_text(text)
    total = len(cleaned)

    if total == 0:
        return float("inf")

    score = 0.0

    for letter, expected_percent in ENGLISH_FREQ.items():
        observed = cleaned.count(letter)
        expected = total * expected_percent / 100

        if expected > 0:
            score += ((observed - expected) ** 2) / expected

    return score


def word_bonus(text: str) -> int:
    upper_text = text.upper()
    return sum(upper_text.count(word) for word in COMMON_WORDS)


def english_score(text: str) -> float:
    """
    Lower score is better.
    Chi-square gives frequency score.
    Common words improve the score.
    """
    return chi_square_score(text) - (word_bonus(text) * 10)
