from .text import clean_text

PLAYFAIR_ALPHABET = "ABCDEFGHIKLMNOPQRSTUVWXYZ"


def build_square(key: str) -> list[list[str]]:
    cleaned_key = clean_text(key).replace("J", "I")

    if not cleaned_key:
        raise ValueError("Key must contain at least one A-Z letter.")

    letters = []

    for ch in cleaned_key + PLAYFAIR_ALPHABET:
        if ch not in letters:
            letters.append(ch)

    return [letters[i:i + 5] for i in range(0, 25, 5)]


def find_position(square: list[list[str]], letter: str) -> tuple[int, int]:
    letter = "I" if letter == "J" else letter

    for row in range(5):
        for col in range(5):
            if square[row][col] == letter:
                return row, col

    raise ValueError(f"Letter not found: {letter}")


def prepare_plaintext(text: str) -> str:
    cleaned = clean_text(text).replace("J", "I")

    if not cleaned:
        return ""

    pairs = []
    index = 0

    while index < len(cleaned):
        a = cleaned[index]
        b = cleaned[index + 1] if index + 1 < len(cleaned) else "X"

        if a == b:
            pairs.append(a + "X")
            index += 1
        else:
            pairs.append(a + b)
            index += 2

    return "".join(pairs)


def encrypt_pair(square: list[list[str]], a: str, b: str) -> str:
    row_a, col_a = find_position(square, a)
    row_b, col_b = find_position(square, b)

    if row_a == row_b:
        return square[row_a][(col_a + 1) % 5] + square[row_b][(col_b + 1) % 5]

    if col_a == col_b:
        return square[(row_a + 1) % 5][col_a] + square[(row_b + 1) % 5][col_b]

    return square[row_a][col_b] + square[row_b][col_a]


def decrypt_pair(square: list[list[str]], a: str, b: str) -> str:
    row_a, col_a = find_position(square, a)
    row_b, col_b = find_position(square, b)

    if row_a == row_b:
        return square[row_a][(col_a - 1) % 5] + square[row_b][(col_b - 1) % 5]

    if col_a == col_b:
        return square[(row_a - 1) % 5][col_a] + square[(row_b - 1) % 5][col_b]

    return square[row_a][col_b] + square[row_b][col_a]


def encrypt_playfair(text: str, key: str) -> str:
    square = build_square(key)
    prepared = prepare_plaintext(text)
    result = []

    for i in range(0, len(prepared), 2):
        result.append(encrypt_pair(square, prepared[i], prepared[i + 1]))

    return "".join(result)


def decrypt_playfair(text: str, key: str) -> str:
    square = build_square(key)
    cleaned = clean_text(text).replace("J", "I")

    if len(cleaned) % 2 != 0:
        cleaned += "X"

    result = []

    for i in range(0, len(cleaned), 2):
        result.append(decrypt_pair(square, cleaned[i], cleaned[i + 1]))

    return "".join(result)
