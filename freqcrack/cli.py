import argparse
from pathlib import Path

from freqcrack.core.text import clean_text
from freqcrack.core.frequency import (
    letter_frequency,
    ngram_frequency,
    index_of_coincidence,
)
from freqcrack.core.caesar import crack_caesar
from freqcrack.core.atbash import decrypt_atbash
from freqcrack.core.affine import crack_affine
from freqcrack.core.detect import detect_cipher
from freqcrack.core.vigenere import crack_vigenere
from freqcrack.core.beaufort import crack_beaufort


def read_input(input_value: str) -> str:
    path = Path(input_value)

    if path.exists() and path.is_file():
        return path.read_text(errors="ignore")

    return input_value


def analyze_command(args):
    text = read_input(args.input)
    cleaned = clean_text(text)

    print()
    print("FreqCrack - Frequency Analysis")
    print("=" * 35)
    print(f"Original length : {len(text)}")
    print(f"Cleaned length  : {len(cleaned)}")
    print(f"IC value        : {index_of_coincidence(cleaned)}")
    print()

    print("Top Letters:")
    freqs = letter_frequency(cleaned)
    sorted_freqs = sorted(freqs.items(), key=lambda item: item[1], reverse=True)

    for letter, freq in sorted_freqs[:10]:
        print(f"  {letter}: {freq}%")

    print()
    print("Top Bigrams:")
    for gram, count in ngram_frequency(cleaned, 2, 10):
        print(f"  {gram}: {count}")

    print()
    print("Top Trigrams:")
    for gram, count in ngram_frequency(cleaned, 3, 10):
        print(f"  {gram}: {count}")

    print()


def detect_command(args):
    text = read_input(args.input)
    result = detect_cipher(text)

    print()
    print("FreqCrack - Cipher Detector")
    print("=" * 35)
    print(f"Cleaned length    : {result['length']}")
    print(f"IC value          : {result['ic']}")
    print(f"Repeated trigrams : {result['repeated_trigrams']}")
    print()

    print("Likely cipher types:")
    for index, cipher_type in enumerate(result["likely_types"], start=1):
        print(f"  [{index}] {cipher_type}")

    print()
    print("Solver quick checks:")

    if "best_caesar" in result:
        caesar = result["best_caesar"]
        print(
            f"  Caesar best : shift={caesar['shift']} "
            f"score={caesar['score']}"
        )

    if "best_affine" in result:
        affine = result["best_affine"]
        print(
            f"  Affine best : a={affine['a']} b={affine['b']} "
            f"score={affine['score']}"
        )

    print()
    print("Suggestions:")
    for suggestion in result["suggestions"]:
        print(f"  - {suggestion}")

    print()


def solve_caesar_command(args):
    text = read_input(args.input)
    results = crack_caesar(text, top=args.top)

    print()
    print("FreqCrack - Caesar Solver")
    print("=" * 30)

    for index, result in enumerate(results, start=1):
        print()
        print(f"[{index}] Shift: {result['shift']} | Score: {result['score']}")
        print("-" * 30)
        print(result["plaintext"].strip())

    print()


def solve_atbash_command(args):
    text = read_input(args.input)
    plaintext = decrypt_atbash(text)

    print()
    print("FreqCrack - Atbash Solver")
    print("=" * 30)
    print(plaintext.strip())
    print()


def solve_affine_command(args):
    text = read_input(args.input)
    results = crack_affine(text, top=args.top)

    print()
    print("FreqCrack - Affine Solver")
    print("=" * 30)

    for index, result in enumerate(results, start=1):
        print()
        print(
            f"[{index}] a: {result['a']} | b: {result['b']} | "
            f"Score: {result['score']}"
        )
        print("-" * 30)
        print(result["plaintext"].strip())

    print()


def solve_vigenere_command(args):
    text = read_input(args.input)
    results = crack_vigenere(
        text,
        max_key_length=args.max_key_length,
        top=args.top,
        shift_candidates=args.shift_candidates,
    )

    print()
    print("FreqCrack - Vigenere Solver")
    print("=" * 30)

    for index, result in enumerate(results, start=1):
        print()
        print(
            f"[{index}] Key: {result['key']} | "
            f"Length: {result['key_length']} | "
            f"Avg IC: {result['avg_ic']} | "
            f"Score: {result['score']}"
        )
        print("-" * 30)
        print(result["plaintext"].strip())

    print()


def solve_beaufort_command(args):
    text = read_input(args.input)
    results = crack_beaufort(
        text,
        max_key_length=args.max_key_length,
        top=args.top,
    )

    print()
    print("FreqCrack - Beaufort Solver")
    print("=" * 30)

    for index, result in enumerate(results, start=1):
        print()
        print(
            f"[{index}] Key: {result['key']} | "
            f"Length: {result['key_length']} | "
            f"Avg IC: {result['avg_ic']} | "
            f"Score: {result['score']}"
        )
        print("-" * 30)
        print(result["plaintext"].strip())

    print()


def main():
    parser = argparse.ArgumentParser(
        prog="freqcrack",
        description="A terminal tool for frequency analysis and classical cipher cracking."
    )

    subparsers = parser.add_subparsers(dest="command")

    analyze_parser = subparsers.add_parser(
        "analyze",
        help="Analyze letter, bigram, trigram frequency and IC value."
    )
    analyze_parser.add_argument("input", help="Cipher text or file path")
    analyze_parser.set_defaults(func=analyze_command)

    detect_parser = subparsers.add_parser(
        "detect",
        help="Detect likely classical cipher type."
    )
    detect_parser.add_argument("input", help="Cipher text or file path")
    detect_parser.set_defaults(func=detect_command)

    solve_parser = subparsers.add_parser(
        "solve",
        help="Solve classical ciphers."
    )

    solve_subparsers = solve_parser.add_subparsers(dest="cipher")

    caesar_parser = solve_subparsers.add_parser(
        "caesar",
        help="Crack Caesar cipher by trying all shifts."
    )
    caesar_parser.add_argument("input", help="Cipher text or file path")
    caesar_parser.add_argument("-t", "--top", type=int, default=5)
    caesar_parser.set_defaults(func=solve_caesar_command)

    atbash_parser = solve_subparsers.add_parser(
        "atbash",
        help="Decode Atbash cipher."
    )
    atbash_parser.add_argument("input", help="Cipher text or file path")
    atbash_parser.set_defaults(func=solve_atbash_command)

    affine_parser = solve_subparsers.add_parser(
        "affine",
        help="Crack Affine cipher by trying valid a and b keys."
    )
    affine_parser.add_argument("input", help="Cipher text or file path")
    affine_parser.add_argument("-t", "--top", type=int, default=5)
    affine_parser.set_defaults(func=solve_affine_command)

    vigenere_parser = solve_subparsers.add_parser(
        "vigenere",
        help="Crack Vigenere cipher using frequency analysis."
    )
    vigenere_parser.add_argument("input", help="Cipher text or file path")
    vigenere_parser.add_argument("-t", "--top", type=int, default=5)
    vigenere_parser.add_argument("-m", "--max-key-length", type=int, default=12)
    vigenere_parser.add_argument("-s", "--shift-candidates", type=int, default=5)
    vigenere_parser.set_defaults(func=solve_vigenere_command)

    beaufort_parser = solve_subparsers.add_parser(
        "beaufort",
        help="Crack Beaufort cipher using frequency analysis."
    )
    beaufort_parser.add_argument("input", help="Cipher text or file path")
    beaufort_parser.add_argument("-t", "--top", type=int, default=5)
    beaufort_parser.add_argument("-m", "--max-key-length", type=int, default=12)
    beaufort_parser.set_defaults(func=solve_beaufort_command)

    args = parser.parse_args()

    if not hasattr(args, "func"):
        parser.print_help()
        return

    args.func(args)


if __name__ == "__main__":
    main()
