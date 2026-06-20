from .text import ALPHABET


def decrypt_atbash(text: str) -> str:
    result = []

    reversed_alphabet = ALPHABET[::-1]

    for ch in text:
        upper = ch.upper()

        if upper in ALPHABET:
            index = ALPHABET.index(upper)
            new_char = reversed_alphabet[index]

            if ch.islower():
                result.append(new_char.lower())
            else:
                result.append(new_char)
        else:
            result.append(ch)

    return "".join(result)
