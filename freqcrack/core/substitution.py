import math
import random
from collections import Counter

from .text import ALPHABET, clean_text
from .scoring import english_score

ENGLISH_FREQ_ORDER = "ETAOINSHRDLCUMWFGYPBVKJXQZ"

COMMON_BIGRAMS = [
    "TH", "HE", "IN", "ER", "AN", "RE", "ON", "AT", "EN", "ND",
    "TI", "ES", "OR", "TE", "OF", "ED", "IS", "IT", "AL", "AR",
    "ST", "TO", "NT", "NG", "SE", "HA", "AS", "OU", "IO", "LE",
]

COMMON_TRIGRAMS = [
    "THE", "AND", "ING", "HER", "HAT", "HIS", "THA", "ERE", "FOR",
    "ENT", "ION", "TER", "WAS", "YOU", "ITH", "VER", "ALL", "WIT",
    "THI", "TIO", "ESS", "AGE", "FRE", "REQ", "QUE", "ENC", "NCY",
]

COMMON_WORDS = [
    "THE", "AND", "THIS", "THAT", "HAVE", "WITH", "MESSAGE", "CIPHER",
    "FREQUENCY", "ANALYSIS", "CLASSICAL", "SOLVE", "TOOL", "HELLO",
    "WORLD", "TEST", "FOR", "FROM", "LETTER", "CRACK", "FREQCRACK",
    "SECRET", "CAN", "ANALYZE", "COMMON", "WORDS", "BIGRAMS",
    "TRIGRAMS", "ENGLISH", "SCORING", "HELP",
]


def build_frequency_mapping(text: str) -> dict:
    cleaned = clean_text(text)
    counts = Counter(cleaned)

    cipher_order = [letter for letter, _ in counts.most_common()]

    for letter in ALPHABET:
        if letter not in cipher_order:
            cipher_order.append(letter)

    mapping = {}

    for cipher_letter, plain_letter in zip(cipher_order, ENGLISH_FREQ_ORDER):
        mapping[cipher_letter] = plain_letter

    return mapping


def build_atbash_mapping() -> dict:
    return {
        cipher_letter: plain_letter
        for cipher_letter, plain_letter in zip(ALPHABET, ALPHABET[::-1])
    }


def build_identity_mapping() -> dict:
    return {
        letter: letter
        for letter in ALPHABET
    }


def build_caesar_mapping(shift: int) -> dict:
    """
    Mapping is cipher letter -> plaintext letter.
    """
    mapping = {}

    for index, cipher_letter in enumerate(ALPHABET):
        plain_index = (index - shift) % 26
        mapping[cipher_letter] = ALPHABET[plain_index]

    return mapping


def starting_mappings(text: str) -> list:
    mappings = [
        build_frequency_mapping(text),
        build_atbash_mapping(),
        build_identity_mapping(),
    ]

    for shift in range(26):
        mappings.append(build_caesar_mapping(shift))

    unique = []
    seen = set()

    for mapping in mappings:
        signature = tuple(mapping[letter] for letter in ALPHABET)

        if signature not in seen:
            seen.add(signature)
            unique.append(mapping)

    return unique


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


def swap_mapping(mapping: dict, a: str, b: str) -> dict:
    new_mapping = mapping.copy()
    new_mapping[a], new_mapping[b] = new_mapping[b], new_mapping[a]
    return new_mapping


def substitution_score(text: str) -> float:
    """
    Lower is better.
    Uses normal English score plus bonuses for common bigrams,
    trigrams, and words.
    """
    cleaned = clean_text(text)
    score = english_score(text)

    for gram in COMMON_BIGRAMS:
        score -= cleaned.count(gram) * 2

    for gram in COMMON_TRIGRAMS:
        score -= cleaned.count(gram) * 6

    upper_text = text.upper()

    for word in COMMON_WORDS:
        score -= upper_text.count(word) * 15

    return score


def randomize_mapping(mapping: dict, swaps: int = 20) -> dict:
    new_mapping = mapping.copy()

    for _ in range(swaps):
        a, b = random.sample(list(ALPHABET), 2)
        new_mapping = swap_mapping(new_mapping, a, b)

    return new_mapping


def evaluate_mapping(text: str, mapping: dict) -> dict:
    plaintext = decrypt_with_mapping(text, mapping)
    score = substitution_score(plaintext)

    return {
        "score": score,
        "mapping": mapping,
        "plaintext": plaintext,
    }


def crack_substitution_frequency(text: str) -> dict:
    mapping = build_frequency_mapping(text)
    plaintext = decrypt_with_mapping(text, mapping)
    score = substitution_score(plaintext)

    return {
        "method": "frequency-order guess",
        "score": round(score, 2),
        "mapping": mapping,
        "mapping_text": format_mapping(mapping),
        "plaintext": plaintext,
    }


def crack_substitution_hillclimb(
    text: str,
    restarts: int = 30,
    iterations: int = 5000,
    seed: int | None = 1337,
) -> dict:
    if seed is not None:
        random.seed(seed)

    start_maps = starting_mappings(text)

    best = None

    for mapping in start_maps:
        result = evaluate_mapping(text, mapping)

        if best is None or result["score"] < best["score"]:
            best = result

    base_mapping = best["mapping"]

    restart_mappings = start_maps.copy()

    for restart in range(restarts):
        restart_mappings.append(
            randomize_mapping(base_mapping, swaps=restart + 5)
        )

    for current_mapping in restart_mappings:
        current_plaintext = decrypt_with_mapping(text, current_mapping)
        current_score = substitution_score(current_plaintext)

        temperature = 25.0

        for _ in range(iterations):
            a, b = random.sample(list(ALPHABET), 2)
            candidate_mapping = swap_mapping(current_mapping, a, b)
            candidate_plaintext = decrypt_with_mapping(text, candidate_mapping)
            candidate_score = substitution_score(candidate_plaintext)

            improved = candidate_score < current_score

            probability = math.exp(
                min(0, (current_score - candidate_score) / temperature)
            )

            if improved or random.random() < probability:
                current_mapping = candidate_mapping
                current_score = candidate_score
                current_plaintext = candidate_plaintext

            if current_score < best["score"]:
                best = {
                    "score": current_score,
                    "mapping": current_mapping,
                    "plaintext": current_plaintext,
                }

            temperature *= 0.9995

    return {
        "method": "hill-climbing substitution crack",
        "score": round(best["score"], 2),
        "mapping": best["mapping"],
        "mapping_text": format_mapping(best["mapping"]),
        "plaintext": best["plaintext"],
    }
