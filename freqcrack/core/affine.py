from math import gcd

from .text import ALPHABET
from .scoring import english_score

VALID_A_VALUES = [a for a in range(26) if gcd(a, 26) == 1]


def mod_inverse(a: int, m: int = 26) -> int:
    for x in range(1, m):
        if (a * x) % m == 1:
            return x

    raise ValueError(f"No modular inverse for a={a}")


def decrypt_affine(text: str, a: int, b: int) -> str:
    """
    Affine decryption:
    D(y) = a^-1 * (y - b) mod 26
    """
    a_inv = mod_inverse(a, 26)
    result = []

    for ch in text:
        upper = ch.upper()

        if upper in ALPHABET:
            y = ALPHABET.index(upper)
            x = (a_inv * (y - b)) % 26
            new_char = ALPHABET[x]

            if ch.islower():
                result.append(new_char.lower())
            else:
                result.append(new_char)
        else:
            result.append(ch)

    return "".join(result)


def encrypt_affine(text: str, a: int, b: int) -> str:
    result = []

    for ch in text:
        upper = ch.upper()

        if upper in ALPHABET:
            x = ALPHABET.index(upper)
            y = (a * x + b) % 26
            new_char = ALPHABET[y]

            if ch.islower():
                result.append(new_char.lower())
            else:
                result.append(new_char)
        else:
            result.append(ch)

    return "".join(result)


def crack_affine(text: str, top: int = 5) -> list:
    results = []

    for a in VALID_A_VALUES:
        for b in range(26):
            plaintext = decrypt_affine(text, a, b)
            score = english_score(plaintext)

            results.append({
                "a": a,
                "b": b,
                "score": round(score, 2),
                "plaintext": plaintext,
            })

    return sorted(results, key=lambda item: item["score"])[:top]
