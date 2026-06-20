from .text import ALPHABET


def decrypt_rot(text: str, shift: int = 13) -> str:
    result = []

    for ch in text:
        upper = ch.upper()

        if upper in ALPHABET:
            old_index = ALPHABET.index(upper)
            new_index = (old_index - shift) % 26
            new_char = ALPHABET[new_index]

            result.append(new_char.lower() if ch.islower() else new_char)
        else:
            result.append(ch)

    return "".join(result)


def decrypt_rot47(text: str) -> str:
    result = []

    for ch in text:
        code = ord(ch)

        if 33 <= code <= 126:
            result.append(chr(33 + ((code - 33 + 47) % 94)))
        else:
            result.append(ch)

    return "".join(result)
