from itertools import product

from .text import ALPHABET, clean_text
from .frequency import index_of_coincidence
from .scoring import chi_square_score, english_score


def clean_key(key: str) -> str:
    key_clean = clean_text(key)

    if not key_clean:
        raise ValueError("Key must contain at least one A-Z letter.")

    return key_clean


def decrypt_beaufort(text: str, key: str) -> str:
    """
    Beaufort cipher:
    plaintext = key - ciphertext mod 26

    Beaufort encryption and decryption use the same operation.
    """
    key_clean = clean_key(key)
    result = []
    key_index = 0

    for ch in text:
        upper = ch.upper()

        if upper in ALPHABET:
            c = ALPHABET.index(upper)
            k = ALPHABET.index(key_clean[key_index % len(key_clean)])
            p = (k - c) % 26
            new_char = ALPHABET[p]

            if ch.islower():
                result.append(new_char.lower())
            else:
                result.append(new_char)

            key_index += 1
        else:
            result.append(ch)

    return "".join(result)


def encrypt_beaufort(text: str, key: str) -> str:
    return decrypt_beaufort(text, key)


def average_ic_for_key_length(text: str, key_length: int) -> float:
    cleaned = clean_text(text)

    if key_length <= 0:
        return 0.0

    ic_values = []

    for index in range(key_length):
        column = cleaned[index::key_length]

        if len(column) > 1:
            ic_values.append(index_of_coincidence(column))

    if not ic_values:
        return 0.0

    return round(sum(ic_values) / len(ic_values), 4)


def top_key_letters_for_column(column: str, top: int = 5) -> list:
    results = []

    for key_index in range(26):
        key_letter = ALPHABET[key_index]
        plaintext = decrypt_beaufort(column, key_letter)
        score = chi_square_score(plaintext)

        results.append((key_letter, score))

    return sorted(results, key=lambda item: item[1])[:top]


def candidate_keys_for_length(
    text: str,
    key_length: int,
    key_candidates: int = 5,
    max_combinations: int = 100000,
) -> list:
    cleaned = clean_text(text)
    columns = [cleaned[index::key_length] for index in range(key_length)]

    key_options = [
        top_key_letters_for_column(column, top=key_candidates)
        for column in columns
    ]

    total_combinations = 1

    for options in key_options:
        total_combinations *= len(options)

    if total_combinations > max_combinations:
        greedy_key = "".join(options[0][0] for options in key_options)
        return [greedy_key]

    option_lists = [
        [letter for letter, _ in options]
        for options in key_options
    ]

    keys = []

    for combination in product(*option_lists):
        keys.append("".join(combination))

    return keys


def crack_beaufort(
    text: str,
    max_key_length: int = 12,
    top: int = 5,
    key_candidates: int = 5,
) -> list:
    results = []
    seen_keys = set()

    for key_length in range(1, max_key_length + 1):
        keys = candidate_keys_for_length(
            text,
            key_length,
            key_candidates=key_candidates,
        )

        for key in keys:
            if key in seen_keys:
                continue

            seen_keys.add(key)
            plaintext = decrypt_beaufort(text, key)
            score = english_score(plaintext)

            results.append({
                "key_length": key_length,
                "key": key,
                "avg_ic": average_ic_for_key_length(text, key_length),
                "score": round(score, 2),
                "plaintext": plaintext,
            })

    return sorted(results, key=lambda item: item["score"])[:top]
