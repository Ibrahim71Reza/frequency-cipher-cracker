from collections import Counter

from .text import ALPHABET, clean_text
from .scoring import english_score

ENGLISH_FREQ_ORDER = "ETAOINSHRDLCUMWFGYPBVKJXQZ"


def build_frequency_mapping(text: str) -> dict:
    """
    Build a simple monoalphabetic substitution guess by mapping
    the most common ciphertext letters to common English letters.
    """
    cleaned = clean_text(text)
    counts = Counter(cleaned)

    cipher_order = [
        letter for letter, _ in counts.most_common()
    ]

    for letter in ALPHABET:
        if letter not in cipher_order:
            cipher_order.append(letter)

    mapping = {}

    for cipher_letter, plain_letter in zip(cipher_order, ENGLISH_FREQ_ORDER):
        mapping[cipher_letter] = plain_letter

    return mapping


def decrypt_with_mapping(text: str, mapping: dict) -> str:
    result = []

    for ch in text:
        upper = ch.upper()

        if upper in ALPHABET:
            new_char = mapping.get(upper, upper)

            if ch.islower():
                result.append(new_char.lower())
            else:
                result.append(new_char)
        else:
            result.append(ch)

    return "".join(result)


def format_mapping(mapping: dict) -> str:
    parts = []

    for cipher_letter in ALPHABET:
        parts.append(f"{cipher_letter}->{mapping.get(cipher_letter, '?')}")

    return " ".join(parts)


def crack_substitution_frequency(text: str) -> dict:
    mapping = build_frequency_mapping(text)
    plaintext = decrypt_with_mapping(text, mapping)
    score = english_score(plaintext)

    return {
        "method": "frequency-order guess",
        "score": round(score, 2),
        "mapping": mapping,
        "mapping_text": format_mapping(mapping),
        "plaintext": plaintext,
    }
