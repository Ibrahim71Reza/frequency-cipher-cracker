# FreqCrack Accuracy Report

## Benchmark Summary

The ultimate benchmark was created to test practical solver accuracy against harder generated ciphertext samples.

## Current Result

- Unit tests: 16/16 passing
- Ultimate benchmark: 13/16 passing

## Passed Benchmark Areas

- Caesar
- Atbash
- Affine
- Rail Fence
- Columnar Transposition
- ROT13
- ROT47
- Keyword Substitution
- Playfair
- Autokey Vigenere
- Polybius Square
- Baconian
- Detector smoke test

## Areas Needing Future Improvement

### Vigenere

The solver found a near-correct key but missed several letters.

Expected:

FORTIFICATION

Detected:

FORTOFICATIQN

### Beaufort

The solver also found a near-correct key but missed several letters.

Expected:

FORTIFICATION

Detected:

FORTCFICATIMN

### Advanced Substitution

The solver produced highly readable plaintext, but still had small letter errors such as:

- INDEW instead of INDEX
- BORD instead of WORD

## Interpretation

FreqCrack v0.2.0 is stable and useful for classical cipher practice. The benchmark shows strong performance on most supported ciphers, while advanced Vigenere, Beaufort, and general substitution cracking need stronger scoring and faster key-refinement algorithms in a future release.

## Future Accuracy Goals

- Improve Vigenere key refinement
- Improve Beaufort key refinement
- Add quadgram or tetragram scoring
- Add better word-pattern correction
- Add benchmark scoring with partial-credit accuracy
- Add optional high-power mode for long ciphertexts
