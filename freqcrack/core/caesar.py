from .text import ALPHABET
from .scoring import english_score


def decrypt_caesar(text: str, shift: int) -> str:
    result = []

    for ch in text:
        upper = ch.upper()

        if upper in ALPHABET:
            old_index = ALPHABET.index(upper)
            new_index = (old_index - shift) % 26
            new_char = ALPHABET[new_index]

            if ch.islower():
                result.append(new_char.lower())
            else:
                result.append(new_char)
        else:
            result.append(ch)

    return "".join(result)


def crack_caesar(text: str, top: int = 5) -> list:
    results = []

    for shift in range(26):
        plaintext = decrypt_caesar(text, shift)
        score = english_score(plaintext)

        results.append({
            "shift": shift,
            "score": round(score, 2),
            "plaintext": plaintext,
        })

    return sorted(results, key=lambda item: item["score"])[:top]
