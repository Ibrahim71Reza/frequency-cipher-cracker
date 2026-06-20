# Frequency Cipher Cracker

`freqcrack` is a Kali Linux terminal tool for frequency analysis and classical cipher cracking.

## Features

- Letter frequency analysis
- Bigram and trigram analysis
- Index of Coincidence calculation
- Basic cipher detection
- Caesar cipher solver
- Atbash cipher solver
- Affine cipher solver
- Vigenere cipher solver
- Beaufort cipher solver
- Rail Fence cipher solver
- Columnar Transposition cipher solver
- Monoalphabetic substitution frequency solver
- Advanced substitution solver using hill-climbing

## Installation

Create and activate a Python virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate

Install the project locally:

pip install -e .
Usage

Analyze ciphertext:

freqcrack analyze samples/sample_caesar.txt

Detect likely cipher type:

freqcrack detect samples/sample_caesar.txt

Solve Caesar cipher:

freqcrack solve caesar samples/sample_caesar.txt

Solve Atbash cipher:

freqcrack solve atbash samples/sample_atbash.txt

Solve Affine cipher:

freqcrack solve affine samples/sample_affine.txt

Solve Vigenere cipher:

freqcrack solve vigenere samples/sample_vigenere.txt

Solve Beaufort cipher:

freqcrack solve beaufort samples/sample_beaufort.txt

Solve Rail Fence cipher:

freqcrack solve railfence samples/sample_railfence.txt

Solve Columnar Transposition cipher:

freqcrack solve columnar samples/sample_columnar.txt

Solve Monoalphabetic Substitution cipher:

freqcrack solve substitution samples/sample_substitution.txt

Use advanced substitution solving:

freqcrack solve substitution --advanced samples/sample_substitution.txt

Solve ROT13 cipher:

freqcrack solve rot samples/sample_rot13.txt

Solve ROT47 cipher:

freqcrack solve rot --rot47 samples/sample_rot47.txt

Solve Keyword Substitution cipher:

freqcrack solve keyword samples/sample_keyword.txt --key CIPHER

Solve Playfair cipher:

freqcrack solve playfair samples/sample_playfair.txt --key "PLAYFAIR EXAMPLE"

Solve Autokey Vigenere cipher:

freqcrack solve autokey samples/sample_autokey.txt --key QUEENLY

Solve Polybius Square cipher:

freqcrack solve polybius samples/sample_polybius.txt

Solve Baconian cipher:

freqcrack solve baconian samples/sample_baconian.txt
Running Tests
python3 -m unittest discover -s tests -p "test_*.py" -v
Project Goal

The goal of this project is to build an ultimate frequency-analysis terminal tool for Kali Linux that can analyze, detect, and crack classical ciphers.

Disclaimer

This tool is for educational, research, and CTF-style classical cryptography practice only.
