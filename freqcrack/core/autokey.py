from .text import ALPHABET, clean_text


def clean_key(key: str) -> str:
    cleaned = clean_text(key)

    if not cleaned:
        raise ValueError("Key must contain at least one A-Z letter.")

    return cleaned


def encrypt_autokey(text: str, key: str) -> str:
    key_clean = clean_key(key)
    key_stream = list(key_clean)
    plaintext_letters = []
    result = []
    key_index = 0

    for ch in text:
        upper = ch.upper()

        if upper in ALPHABET:
            plaintext_letters.append(upper)

            if key_index >= len(key_stream):
                key_stream.append(plaintext_letters[key_index - len(key_clean)])

            shift = ALPHABET.index(key_stream[key_index])
            plain_index = ALPHABET.index(upper)
            cipher_char = ALPHABET[(plain_index + shift) % 26]

            result.append(cipher_char.lower() if ch.islower() else cipher_char)
            key_index += 1
        else:
            result.append(ch)

    return "".join(result)


def decrypt_autokey(text: str, key: str) -> str:
    key_stream = list(clean_key(key))
    result = []
    key_index = 0

    for ch in text:
        upper = ch.upper()

        if upper in ALPHABET:
            shift = ALPHABET.index(key_stream[key_index])
            cipher_index = ALPHABET.index(upper)
            plain_char = ALPHABET[(cipher_index - shift) % 26]

            result.append(plain_char.lower() if ch.islower() else plain_char)
            key_stream.append(plain_char)
            key_index += 1
        else:
            result.append(ch)

    return "".join(result)
