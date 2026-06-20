import argparse
from pathlib import Path

from freqcrack.core.text import clean_text
from freqcrack.core.frequency import (
    letter_frequency,
    ngram_frequency,
    index_of_coincidence,
)
from freqcrack.core.caesar import crack_caesar


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
    caesar_parser.add_argument(
        "-t",
        "--top",
        type=int,
        default=5,
        help="Number of best results to show."
    )
    caesar_parser.set_defaults(func=solve_caesar_command)

    args = parser.parse_args()

    if not hasattr(args, "func"):
        parser.print_help()
        return

    args.func(args)


if __name__ == "__main__":
    main()
