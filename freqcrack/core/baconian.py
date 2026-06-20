from .text import clean_text

BACON_ALPHABET = "ABCDEFGHIKLMNOPQRSTUWXYZ"


def index_to_bacon(index: int) -> str:
    bits = format(index, "05b")
    return bits.replace("0", "A").replace("1", "B")


def bacon_to_index(group: str) -> int:
    bits = group.replace("A", "0").replace("B", "1")
    return int(bits, 2)


def encrypt_baconian(text: str) -> str:
    cleaned = clean_text(text).replace("J", "I").replace("V", "U")
    groups = []

    for ch in cleaned:
        if ch in BACON_ALPHABET:
            groups.append(index_to_bacon(BACON_ALPHABET.index(ch)))

    return " ".join(groups)


def decrypt_baconian(text: str) -> str:
    cleaned = "".join(ch for ch in text.upper() if ch in "AB")
    result = []

    for i in range(0, len(cleaned) - 4, 5):
        group = cleaned[i:i + 5]
        index = bacon_to_index(group)

        if 0 <= index < len(BACON_ALPHABET):
            result.append(BACON_ALPHABET[index])

    return "".join(result)
