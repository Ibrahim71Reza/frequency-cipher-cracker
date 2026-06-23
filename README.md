<div align="center">
# Frequency Cipher Cracker

![Python](https://img.shields.io/badge/Python-3.x-blue)
![Platform](https://img.shields.io/badge/Platform-Kali%20Linux-darkgreen)
![Version](https://img.shields.io/badge/Version-0.2.1-purple)
![License](https://img.shields.io/badge/License-MIT-yellow)
![Tests](https://img.shields.io/badge/Tests-16%2F16%20Passing-brightgreen)

`freqcrack` is a Kali Linux terminal tool for **frequency analysis**, **cipher detection**, and **classical cipher cracking**.

It is designed for cryptography practice, CTF learning, and educational research.

---

## Overview

`freqcrack` helps analyze and solve classical ciphers directly from the terminal.

It supports frequency analysis, Index of Coincidence, cipher detection hints, known-key decoders, and automated cracking for several classical cipher families.

---

## Features

### Analysis Tools

| Feature              | Description                                             |
| -------------------- | ------------------------------------------------------- |
| Letter frequency     | Shows most common letters in the ciphertext             |
| Bigram analysis      | Shows repeated 2-letter patterns                        |
| Trigram analysis     | Shows repeated 3-letter patterns                        |
| Index of Coincidence | Helps identify monoalphabetic vs polyalphabetic ciphers |
| Cipher detection     | Gives likely cipher-type suggestions                    |

### Supported Cipher Solvers

| Cipher                      | Command                                   |
| --------------------------- | ----------------------------------------- |
| Caesar                      | `freqcrack solve caesar`                  |
| Atbash                      | `freqcrack solve atbash`                  |
| Affine                      | `freqcrack solve affine`                  |
| Vigenere                    | `freqcrack solve vigenere`                |
| Beaufort                    | `freqcrack solve beaufort`                |
| Rail Fence                  | `freqcrack solve railfence`               |
| Columnar Transposition      | `freqcrack solve columnar`                |
| Monoalphabetic Substitution | `freqcrack solve substitution`            |
| Advanced Substitution       | `freqcrack solve substitution --advanced` |
| ROT13 / ROT                 | `freqcrack solve rot`                     |
| ROT47                       | `freqcrack solve rot --rot47`             |
| Keyword Substitution        | `freqcrack solve keyword`                 |
| Playfair                    | `freqcrack solve playfair`                |
| Autokey Vigenere            | `freqcrack solve autokey`                 |
| Polybius Square             | `freqcrack solve polybius`                |
| Baconian                    | `freqcrack solve baconian`                |

---

</div>

## Project Structure

```text
frequency-cipher-cracker/
├── freqcrack/                  # Main Python package
│   ├── cli.py                  # Command-line interface
│   └── core/                   # Cipher logic and analysis modules
├── samples/                    # Sample ciphertext files
├── tests/                      # Unit tests
├── benchmarks/                 # Accuracy benchmark files
├── ACCURACY_REPORT.md          # Benchmark result summary
├── CHANGELOG.md                # Version history
├── LICENSE                     # MIT License
├── pyproject.toml              # Python project config
└── README.md                   # Project documentation
```

---

## Installation

Clone the repository:

```bash
git clone https://github.com/Ibrahim71Reza/frequency-cipher-cracker.git
cd frequency-cipher-cracker
```

Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install the project locally:

```bash
pip install -e .
```

Check installation:

```bash
freqcrack --version
```

Expected output:

```text
freqcrack 0.2.1
```

---

## Basic Usage

### Analyze Ciphertext

```bash
freqcrack analyze samples/sample_caesar.txt
```

This shows:

```text
Letter frequency
Top bigrams
Top trigrams
Index of Coincidence
```

---

### Detect Likely Cipher Type

```bash
freqcrack detect samples/sample_caesar.txt
```

This gives likely cipher categories and suggested solver commands.

---

## Solver Examples

### Caesar Cipher

```bash
freqcrack solve caesar samples/sample_caesar.txt
```

---

### Atbash Cipher

```bash
freqcrack solve atbash samples/sample_atbash.txt
```

---

### Affine Cipher

```bash
freqcrack solve affine samples/sample_affine.txt
```

---

### Vigenere Cipher

```bash
freqcrack solve vigenere samples/sample_vigenere.txt
```

Optional settings:

```bash
freqcrack solve vigenere samples/sample_vigenere.txt --max-key-length 12 --shift-candidates 5
```

---

### Beaufort Cipher

```bash
freqcrack solve beaufort samples/sample_beaufort.txt
```

Optional settings:

```bash
freqcrack solve beaufort samples/sample_beaufort.txt --max-key-length 12 --key-candidates 5
```

---

### Rail Fence Cipher

```bash
freqcrack solve railfence samples/sample_railfence.txt
```

---

### Columnar Transposition Cipher

```bash
freqcrack solve columnar samples/sample_columnar.txt
```

Optional settings:

```bash
freqcrack solve columnar samples/sample_columnar.txt --max-columns 7 --max-permutations 5040
```

---

### Monoalphabetic Substitution Cipher

```bash
freqcrack solve substitution samples/sample_substitution.txt
```

Advanced hill-climbing mode:

```bash
freqcrack solve substitution --advanced samples/sample_substitution.txt
```

---

### ROT13 Cipher

```bash
freqcrack solve rot samples/sample_rot13.txt
```

Custom ROT shift:

```bash
freqcrack solve rot samples/sample_rot13.txt --shift 13
```

---

### ROT47 Cipher

```bash
freqcrack solve rot --rot47 samples/sample_rot47.txt
```

---

### Keyword Substitution Cipher

```bash
freqcrack solve keyword samples/sample_keyword.txt --key CIPHER
```

---

### Playfair Cipher

```bash
freqcrack solve playfair samples/sample_playfair.txt --key "PLAYFAIR EXAMPLE"
```

---

### Autokey Vigenere Cipher

```bash
freqcrack solve autokey samples/sample_autokey.txt --key QUEENLY
```

---

### Polybius Square Cipher

```bash
freqcrack solve polybius samples/sample_polybius.txt
```

---

### Baconian Cipher

```bash
freqcrack solve baconian samples/sample_baconian.txt
```

---

## Help Menu

Show all main commands:

```bash
freqcrack --help
```

Show all solver commands:

```bash
freqcrack solve --help
```

---

## Running Tests

Run the full unit test suite:

```bash
python3 -m unittest discover -s tests -p "test_*.py" -v
```

Current test status:

```text
16/16 tests passing
```

---

## Accuracy Benchmark

Run the ultimate accuracy benchmark:

```bash
python3 benchmarks/ultimate_accuracy_test.py
```

Current benchmark summary:

```text
Unit tests: 16/16 passing
Hard benchmark: 13/16 passing
```

See the full accuracy notes:

```text
ACCURACY_REPORT.md
```

---

## Current Accuracy Notes

The tool performs strongly on:

* Caesar
* Atbash
* Affine
* Rail Fence
* Columnar Transposition
* ROT13
* ROT47
* Keyword Substitution
* Playfair
* Autokey
* Polybius
* Baconian
* Basic detection hints

Areas planned for future improvement:

* Long-key Vigenere refinement
* Long-key Beaufort refinement
* Stronger substitution scoring
* Quadgram or tetragram scoring
* Better word-pattern correction
* Optional high-power cracking mode

---

## Version History

| Version  | Description                         |
| -------- | ----------------------------------- |
| `v0.1.0` | Initial working release             |
| `v0.2.0` | Added more classical cipher solvers |
| `v0.2.1` | Added accuracy benchmark and report |

---

## Project Goal

The goal of this project is to build a practical terminal-based classical cryptography tool for Kali Linux.

`freqcrack` is intended to help users:

* Learn frequency analysis
* Practice classical cipher solving
* Understand cipher detection
* Test solver accuracy
* Explore cryptography in a CTF-style workflow

---

## Disclaimer

This tool is for **educational, research, and CTF-style classical cryptography practice only**.

Do not use this tool for unauthorized access, illegal activity, or attacking real systems.

---

## License

This project is licensed under the MIT License.

See:

```text
LICENSE
```

---

## Author

Created by **Ibrahim71Reza**.

GitHub repository:

```text
https://github.com/Ibrahim71Reza/frequency-cipher-cracker
```
