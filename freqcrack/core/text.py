import string

ALPHABET = string.ascii_uppercase


def clean_text(text: str) -> str:
    """
    Keep only A-Z letters and convert to uppercase.
    """
    return "".join(ch for ch in text.upper() if ch in ALPHABET)
