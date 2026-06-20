import argparse
from pathlib import Path

from freqcrack.core.text import clean_text
from freqcrack.core.frequency import (
    letter_frequency,
    ngram_frequency,
    index_of_coincidence,
)


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

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    args.func(args)


if __name__ == "__main__":
    main()
