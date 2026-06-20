import argparse

from freqcrack import __version__
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
from freqcrack.core.railfence import crack_rail_fence
from freqcrack.core.columnar import crack_columnar
from freqcrack.core.substitution import (
    crack_substitution_frequency,
    crack_substitution_hillclimb,
)
from freqcrack.core.rot import decrypt_rot, decrypt_rot47
from freqcrack.core.keyword import decrypt_keyword
from freqcrack.core.playfair import decrypt_playfair
from freqcrack.core.autokey import decrypt_autokey
from freqcrack.core.polybius import decrypt_polybius


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
        key_candidates=args.key_candidates,
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


def solve_railfence_command(args):
    text = read_input(args.input)
    results = crack_rail_fence(
        text,
        max_rails=args.max_rails,
        top=args.top,
    )

    print()
    print("FreqCrack - Rail Fence Solver")
    print("=" * 30)

    for index, result in enumerate(results, start=1):
        print()
        print(
            f"[{index}] Rails: {result['rails']} | "
            f"Score: {result['score']}"
        )
        print("-" * 30)
        print(result["plaintext"].strip())

    print()


def solve_columnar_command(args):
    text = read_input(args.input)
    results = crack_columnar(
        text,
        max_columns=args.max_columns,
        top=args.top,
        max_permutations=args.max_permutations,
    )

    print()
    print("FreqCrack - Columnar Transposition Solver")
    print("=" * 45)

    if not results:
        print("No results. Try increasing --max-permutations or lowering --max-columns.")
        print()
        return

    for index, result in enumerate(results, start=1):
        order_text = ",".join(str(value) for value in result["order"])

        print()
        print(
            f"[{index}] Columns: {result['columns']} | "
            f"Order: {order_text} | "
            f"Score: {result['score']}"
        )
        print("-" * 45)
        print(result["plaintext"].strip())

    print()


def solve_substitution_command(args):
    text = read_input(args.input)

    if args.advanced:
        result = crack_substitution_hillclimb(
            text,
            restarts=args.restarts,
            iterations=args.iterations,
            seed=args.seed,
        )
        title = "FreqCrack - Advanced Substitution Solver"
    else:
        result = crack_substitution_frequency(text)
        title = "FreqCrack - Substitution Frequency Solver"

    print()
    print(title)
    print("=" * 45)
    print(f"Method: {result['method']}")
    print(f"Score : {result['score']}")
    print()
    print("Guessed mapping:")
    print(result["mapping_text"])
    print()
    print("Plaintext guess:")
    print("-" * 45)
    print(result["plaintext"].strip())
    print()

    if not args.advanced:
        print("Note: Use --advanced for hill-climbing substitution cracking.")
        print()


def solve_rot_command(args):
    text = read_input(args.input)

    if args.rot47:
        plaintext = decrypt_rot47(text)
        title = "FreqCrack - ROT47 Solver"
    else:
        plaintext = decrypt_rot(text, args.shift)
        title = f"FreqCrack - ROT Solver Shift {args.shift}"

    print()
    print(title)
    print("=" * 35)
    print(plaintext.strip())
    print()


def solve_keyword_command(args):
    text = read_input(args.input)
    plaintext = decrypt_keyword(text, args.key)

    print()
    print("FreqCrack - Keyword Substitution Solver")
    print("=" * 45)
    print(f"Key: {args.key}")
    print("-" * 45)
    print(plaintext.strip())
    print()


def solve_playfair_command(args):
    text = read_input(args.input)
    plaintext = decrypt_playfair(text, args.key)

    print()
    print("FreqCrack - Playfair Solver")
    print("=" * 35)
    print(f"Key: {args.key}")
    print("-" * 35)
    print(plaintext.strip())
    print()


def solve_autokey_command(args):
    text = read_input(args.input)
    plaintext = decrypt_autokey(text, args.key)

    print()
    print("FreqCrack - Autokey Solver")
    print("=" * 35)
    print(f"Key: {args.key}")
    print("-" * 35)
    print(plaintext.strip())
    print()


def solve_polybius_command(args):
    text = read_input(args.input)
    plaintext = decrypt_polybius(text)

    print()
    print("FreqCrack - Polybius Solver")
    print("=" * 35)
    print(plaintext.strip())
    print()


def main():
    parser = argparse.ArgumentParser(
        prog="freqcrack",
        description="A terminal tool for frequency analysis and classical cipher cracking."
    )

    parser.add_argument(
        "-V",
        "--version",
        action="version",
        version=f"freqcrack {__version__}",
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
    beaufort_parser.add_argument("-k", "--key-candidates", type=int, default=5)
    beaufort_parser.set_defaults(func=solve_beaufort_command)

    railfence_parser = solve_subparsers.add_parser(
        "railfence",
        help="Crack Rail Fence cipher by trying rail counts."
    )
    railfence_parser.add_argument("input", help="Cipher text or file path")
    railfence_parser.add_argument("-t", "--top", type=int, default=5)
    railfence_parser.add_argument("-m", "--max-rails", type=int, default=10)
    railfence_parser.set_defaults(func=solve_railfence_command)

    columnar_parser = solve_subparsers.add_parser(
        "columnar",
        help="Crack Columnar Transposition cipher by trying column orders."
    )
    columnar_parser.add_argument("input", help="Cipher text or file path")
    columnar_parser.add_argument("-t", "--top", type=int, default=5)
    columnar_parser.add_argument("-m", "--max-columns", type=int, default=7)
    columnar_parser.add_argument(
        "-p",
        "--max-permutations",
        type=int,
        default=5040,
        help="Maximum permutations allowed per column size."
    )
    columnar_parser.set_defaults(func=solve_columnar_command)

    substitution_parser = solve_subparsers.add_parser(
        "substitution",
        help="Guess Monoalphabetic Substitution cipher using letter frequency."
    )
    substitution_parser.add_argument("input", help="Cipher text or file path")
    substitution_parser.add_argument(
        "-a",
        "--advanced",
        action="store_true",
        help="Use hill-climbing to improve the substitution mapping."
    )
    substitution_parser.add_argument(
        "-r",
        "--restarts",
        type=int,
        default=30,
        help="Number of hill-climbing restarts."
    )
    substitution_parser.add_argument(
        "-i",
        "--iterations",
        type=int,
        default=5000,
        help="Iterations per restart."
    )
    substitution_parser.add_argument(
        "--seed",
        type=int,
        default=1337,
        help="Random seed for reproducible results."
    )
    substitution_parser.set_defaults(func=solve_substitution_command)

    rot_parser = solve_subparsers.add_parser(
        "rot",
        help="Decode ROT, ROT13, or ROT47 ciphers."
    )
    rot_parser.add_argument("input", help="Cipher text or file path")
    rot_parser.add_argument(
        "-s",
        "--shift",
        type=int,
        default=13,
        help="ROT shift value. Default is 13."
    )
    rot_parser.add_argument(
        "--rot47",
        action="store_true",
        help="Decode using ROT47 instead of alphabetic ROT."
    )
    rot_parser.set_defaults(func=solve_rot_command)

    keyword_parser = solve_subparsers.add_parser(
        "keyword",
        help="Decode Keyword Substitution cipher with a known key."
    )
    keyword_parser.add_argument("input", help="Cipher text or file path")
    keyword_parser.add_argument(
        "-k",
        "--key",
        required=True,
        help="Keyword used to build the substitution alphabet."
    )
    keyword_parser.set_defaults(func=solve_keyword_command)

    playfair_parser = solve_subparsers.add_parser(
        "playfair",
        help="Decode Playfair cipher with a known key."
    )
    playfair_parser.add_argument("input", help="Cipher text or file path")
    playfair_parser.add_argument(
        "-k",
        "--key",
        required=True,
        help="Playfair key phrase."
    )
    playfair_parser.set_defaults(func=solve_playfair_command)

    autokey_parser = solve_subparsers.add_parser(
        "autokey",
        help="Decode Autokey Vigenere cipher with a known key."
    )
    autokey_parser.add_argument("input", help="Cipher text or file path")
    autokey_parser.add_argument(
        "-k",
        "--key",
        required=True,
        help="Autokey starting key."
    )
    autokey_parser.set_defaults(func=solve_autokey_command)

    polybius_parser = solve_subparsers.add_parser(
        "polybius",
        help="Decode Polybius Square cipher."
    )
    polybius_parser.add_argument("input", help="Cipher text or file path")
    polybius_parser.set_defaults(func=solve_polybius_command)

    args = parser.parse_args()

    if not hasattr(args, "func"):
        parser.print_help()
        return

    args.func(args)


if __name__ == "__main__":
    main()
