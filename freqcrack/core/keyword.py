from .text import ALPHABET, clean_text


def build_keyword_alphabet(keyword: str) -> str:
    cleaned_key = clean_text(keyword)

    if not cleaned_key:
        raise ValueError("Keyword must contain at least one A-Z letter.")

    result = []

    for ch in cleaned_key + ALPHABET:
        if ch not in result:
            result.append(ch)

    return "".join(result)


def encrypt_keyword(text: str, keyword: str) -> str:
    cipher_alphabet = build_keyword_alphabet(keyword)
    result = []

    for ch in text:
        upper = ch.upper()

        if upper in ALPHABET:
            index = ALPHABET.index(upper)
            new_char = cipher_alphabet[index]
            result.append(new_char.lower() if ch.islower() else new_char)
        else:
            result.append(ch)

    return "".join(result)


def decrypt_keyword(text: str, keyword: str) -> str:
    cipher_alphabet = build_keyword_alphabet(keyword)
    result = []

    for ch in text:
        upper = ch.upper()

        if upper in cipher_alphabet:
            index = cipher_alphabet.index(upper)
            new_char = ALPHABET[index]
            result.append(new_char.lower() if ch.islower() else new_char)
        else:
            result.append(ch)

    return "".join(result)
