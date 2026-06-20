from .text import clean_text
from .frequency import index_of_coincidence, ngram_frequency
from .caesar import crack_caesar
from .affine import crack_affine


def repeated_ngram_count(text: str, n: int = 3) -> int:
    grams = ngram_frequency(text, n=n, top=1000)
    return sum(1 for _, count in grams if count > 1)


def detect_cipher(text: str) -> dict:
    cleaned = clean_text(text)
    length = len(cleaned)
    ic = index_of_coincidence(cleaned)
    repeated_trigrams = repeated_ngram_count(cleaned, 3)

    suggestions = []
    likely_types = []

    if length == 0:
        return {
            "length": 0,
            "ic": 0.0,
            "repeated_trigrams": 0,
            "likely_types": ["Unknown"],
            "suggestions": ["Input contains no A-Z letters."],
        }

    caesar_best = crack_caesar(text, top=1)[0]
    affine_best = crack_affine(text, top=1)[0]

    if caesar_best["score"] < 40:
        likely_types.append("Caesar / ROT cipher")
        suggestions.append("Try: freqcrack solve caesar <file>")

    if affine_best["score"] < 40:
        likely_types.append("Affine cipher")
        suggestions.append("Try: freqcrack solve affine <file>")

    if 0.055 <= ic <= 0.075:
        likely_types.append("Monoalphabetic substitution or transposition cipher")
        suggestions.append("Try frequency analysis and substitution solving.")

    elif 0.035 <= ic < 0.055:
        likely_types.append("Polyalphabetic cipher, possibly Vigenere")
        suggestions.append("Try Vigenere key-length analysis later.")

    elif ic < 0.035:
        likely_types.append("Very flat frequency distribution")
        suggestions.append("Could be polyalphabetic, random-looking, or too short.")

    if repeated_trigrams > 0:
        likely_types.append("Repeated patterns found, possible Vigenere-style cipher")
        suggestions.append("Repeated trigrams can help estimate key length.")

    if not likely_types:
        likely_types.append("Unknown or text too short")
        suggestions.append("Use: freqcrack analyze <file>")

    return {
        "length": length,
        "ic": ic,
        "repeated_trigrams": repeated_trigrams,
        "likely_types": likely_types,
        "suggestions": suggestions,
        "best_caesar": caesar_best,
        "best_affine": affine_best,
    }
