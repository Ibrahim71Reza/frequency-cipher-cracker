from itertools import permutations
from math import ceil, factorial

from .scoring import english_score


def normalize_columnar_text(text: str) -> str:
    """
    Columnar transposition works on character positions.
    Remove trailing file newlines so they do not affect the grid.
    """
    return text.rstrip("\r\n")


def column_lengths(text_length: int, columns: int) -> list:
    rows = ceil(text_length / columns)
    extra = text_length % columns

    if extra == 0:
        return [rows] * columns

    return [
        rows if column < extra else rows - 1
        for column in range(columns)
    ]


def encrypt_columnar(text: str, order: list[int]) -> str:
    """
    Write text row-wise into columns.
    Read columns according to order.

    Example order [2, 0, 4, 1, 5, 3]
    means read column 2 first, then 0, then 4, etc.
    """
    text = normalize_columnar_text(text)
    columns = len(order)

    if columns <= 1:
        return text

    rows = ceil(len(text) / columns)
    result = []

    for column in order:
        for row in range(rows):
            index = row * columns + column

            if index < len(text):
                result.append(text[index])

    return "".join(result)


def decrypt_columnar(text: str, order: list[int]) -> str:
    text = normalize_columnar_text(text)
    columns = len(order)

    if columns <= 1:
        return text

    lengths = column_lengths(len(text), columns)

    column_data = [""] * columns
    position = 0

    for column in order:
        count = lengths[column]
        column_data[column] = text[position:position + count]
        position += count

    rows = ceil(len(text) / columns)
    result = []

    for row in range(rows):
        for column in range(columns):
            if row < len(column_data[column]):
                result.append(column_data[column][row])

    return "".join(result)


def crack_columnar(
    text: str,
    max_columns: int = 7,
    top: int = 5,
    max_permutations: int = 5040,
) -> list:
    text = normalize_columnar_text(text)
    results = []

    for columns in range(2, max_columns + 1):
        if factorial(columns) > max_permutations:
            continue

        for order in permutations(range(columns)):
            plaintext = decrypt_columnar(text, list(order))
            score = english_score(plaintext)

            results.append({
                "columns": columns,
                "order": list(order),
                "score": round(score, 2),
                "plaintext": plaintext,
            })

    return sorted(results, key=lambda item: item["score"])[:top]
