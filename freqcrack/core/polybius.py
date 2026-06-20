from .text import clean_text

POLYBIUS_ALPHABET = "ABCDEFGHIKLMNOPQRSTUVWXYZ"


def encrypt_polybius(text: str) -> str:
    cleaned = clean_text(text).replace("J", "I")
    pairs = []

    for ch in cleaned:
        index = POLYBIUS_ALPHABET.index(ch)
        row = index // 5 + 1
        col = index % 5 + 1
        pairs.append(f"{row}{col}")

    return " ".join(pairs)


def decrypt_polybius(text: str) -> str:
    digits = [ch for ch in text if ch in "12345"]
    result = []

    for i in range(0, len(digits) - 1, 2):
        row = int(digits[i])
        col = int(digits[i + 1])
        index = (row - 1) * 5 + (col - 1)

        if 0 <= index < len(POLYBIUS_ALPHABET):
            result.append(POLYBIUS_ALPHABET[index])

    return "".join(result)
