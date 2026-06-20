from pathlib import Path

from freqcrack.core.caesar import decrypt_caesar, crack_caesar
from freqcrack.core.atbash import decrypt_atbash
from freqcrack.core.affine import encrypt_affine, crack_affine
from freqcrack.core.vigenere import encrypt_vigenere, crack_vigenere
from freqcrack.core.beaufort import encrypt_beaufort, crack_beaufort
from freqcrack.core.railfence import encrypt_rail_fence, crack_rail_fence
from freqcrack.core.columnar import encrypt_columnar, crack_columnar
from freqcrack.core.substitution import crack_substitution_hillclimb
from freqcrack.core.rot import decrypt_rot, decrypt_rot47
from freqcrack.core.keyword import encrypt_keyword, decrypt_keyword
from freqcrack.core.playfair import encrypt_playfair, decrypt_playfair
from freqcrack.core.autokey import encrypt_autokey, decrypt_autokey
from freqcrack.core.polybius import encrypt_polybius, decrypt_polybius
from freqcrack.core.baconian import encrypt_baconian, decrypt_baconian
from freqcrack.core.detect import detect_cipher


OUT = Path("benchmarks/generated")
OUT.mkdir(parents=True, exist_ok=True)

PLAIN_LONG = (
    "THE FREQCRACK TOOL CAN ANALYZE CLASSICAL CIPHERS USING LETTER FREQUENCY "
    "INDEX OF COINCIDENCE COMMON WORD PATTERNS AND SCORING METHODS. THIS TEST "
    "MESSAGE IS LONG ENOUGH TO GIVE THE SOLVERS MORE STATISTICAL EVIDENCE AND "
    "SHOULD HELP MEASURE PRACTICAL ACCURACY FOR CRYPTOGRAPHY PRACTICE."
)

PLAIN_SHORT = "HELLO WORLD THIS IS A TEST MESSAGE FOR FREQCRACK"

PLAIN_TRANS = "THEFREQCRACKTOOLCANANALYZECLASSICALCIPHERSUSINGLETTERFREQUENCY"


def save(name, text):
    path = OUT / name
    path.write_text(text + "\n")
    return path


def clean_compare(text):
    return "".join(ch for ch in text.upper() if ch.isalpha())


def pass_fail(condition):
    return "PASS" if condition else "FAIL"


def test_caesar():
    ciphertext = decrypt_caesar(PLAIN_LONG, 11)
    save("hard_caesar_shift_11.txt", ciphertext)
    results = crack_caesar(ciphertext, top=5)
    best = results[0]
    ok = clean_compare(PLAIN_LONG) in clean_compare(best["plaintext"])
    return "Caesar", ok, f"best_shift={best['shift']}"


def test_atbash():
    ciphertext = decrypt_atbash(PLAIN_LONG)
    save("hard_atbash.txt", ciphertext)
    plaintext = decrypt_atbash(ciphertext)
    ok = clean_compare(PLAIN_LONG) == clean_compare(plaintext)
    return "Atbash", ok, "known reversible decoder"


def test_affine():
    ciphertext = encrypt_affine(PLAIN_LONG, 7, 3)
    save("hard_affine_a7_b3.txt", ciphertext)
    results = crack_affine(ciphertext, top=5)
    best = results[0]
    ok = clean_compare(PLAIN_LONG) in clean_compare(best["plaintext"])
    return "Affine", ok, f"best_a={best['a']} best_b={best['b']}"


def test_vigenere():
    key = "FORTIFICATION"
    ciphertext = encrypt_vigenere(PLAIN_LONG, key)
    save("hard_vigenere_fortification.txt", ciphertext)
    results = crack_vigenere(ciphertext, max_key_length=14, top=5, shift_candidates=5)
    ok = any(clean_compare(PLAIN_LONG) in clean_compare(item["plaintext"]) for item in results)
    best = results[0]
    return "Vigenere", ok, f"best_key={best['key']}"


def test_beaufort():
    key = "FORTIFICATION"
    ciphertext = encrypt_beaufort(PLAIN_LONG, key)
    save("hard_beaufort_fortification.txt", ciphertext)
    results = crack_beaufort(ciphertext, max_key_length=14, top=5, key_candidates=5)
    ok = any(clean_compare(PLAIN_LONG) in clean_compare(item["plaintext"]) for item in results)
    best = results[0]
    return "Beaufort", ok, f"best_key={best['key']}"


def test_rail_fence():
    ciphertext = encrypt_rail_fence(PLAIN_TRANS, 5)
    save("hard_railfence_5rails.txt", ciphertext)
    results = crack_rail_fence(ciphertext, max_rails=8, top=5)
    ok = any(clean_compare(PLAIN_TRANS) == clean_compare(item["plaintext"]) for item in results)
    best = results[0]
    return "Rail Fence", ok, f"best_rails={best['rails']}"


def test_columnar():
    order = [3, 0, 5, 1, 4, 2]
    ciphertext = encrypt_columnar(PLAIN_TRANS, order)
    save("hard_columnar_6cols.txt", ciphertext)
    results = crack_columnar(ciphertext, max_columns=6, top=5, max_permutations=720)
    ok = any(clean_compare(PLAIN_TRANS) == clean_compare(item["plaintext"]) for item in results)
    best = results[0]
    return "Columnar", ok, f"best_columns={best['columns']} best_order={best['order']}"


def test_rot13():
    ciphertext = decrypt_rot(PLAIN_SHORT, 13)
    save("hard_rot13.txt", ciphertext)
    plaintext = decrypt_rot(ciphertext, 13)
    ok = clean_compare(PLAIN_SHORT) == clean_compare(plaintext)
    return "ROT13", ok, "known reversible decoder"


def test_rot47():
    ciphertext = decrypt_rot47(PLAIN_SHORT)
    save("hard_rot47.txt", ciphertext)
    plaintext = decrypt_rot47(ciphertext)
    ok = PLAIN_SHORT == plaintext
    return "ROT47", ok, "known reversible decoder"


def test_keyword():
    key = "CYBERSECURITY"
    ciphertext = encrypt_keyword(PLAIN_SHORT, key)
    save("hard_keyword_cybersecurity.txt", ciphertext)
    plaintext = decrypt_keyword(ciphertext, key)
    ok = clean_compare(PLAIN_SHORT) == clean_compare(plaintext)
    return "Keyword", ok, f"key={key}"


def test_playfair():
    key = "COMPLEX KEYWORD"
    plaintext = "HIDE THE CRYPTOGRAPHY NOTES INSIDE THE WOODEN DESK"
    ciphertext = encrypt_playfair(plaintext, key)
    save("hard_playfair_complex_keyword.txt", ciphertext)
    decoded = decrypt_playfair(ciphertext, key)
    ok = clean_compare("HIDETHECRYPTOGRAPHYNOTESINSIDETHEWOODENDESK") in clean_compare(decoded).replace("X", "")
    return "Playfair", ok, f"key={key}"


def test_autokey():
    key = "QUEENLY"
    ciphertext = encrypt_autokey(PLAIN_SHORT, key)
    save("hard_autokey_queenly.txt", ciphertext)
    plaintext = decrypt_autokey(ciphertext, key)
    ok = clean_compare(PLAIN_SHORT) == clean_compare(plaintext)
    return "Autokey", ok, f"key={key}"


def test_polybius():
    ciphertext = encrypt_polybius("CRYPTOGRAPHY TEST")
    save("hard_polybius.txt", ciphertext)
    plaintext = decrypt_polybius(ciphertext)
    ok = plaintext == "CRYPTOGRAPHYTEST"
    return "Polybius", ok, "numeric coordinate decoder"


def test_baconian():
    ciphertext = encrypt_baconian("CRYPTOGRAPHY TEST")
    save("hard_baconian.txt", ciphertext)
    plaintext = decrypt_baconian(ciphertext)
    ok = plaintext == "CRYPTOGRAPHYTEST"
    return "Baconian", ok, "A/B group decoder"


def test_substitution_atbash_style():
    ciphertext = decrypt_atbash(PLAIN_LONG)
    save("hard_substitution_atbash_style.txt", ciphertext)
    result = crack_substitution_hillclimb(ciphertext, restarts=30, iterations=5000, seed=1337)
    ok = clean_compare(PLAIN_LONG) in clean_compare(result["plaintext"])
    return "Advanced Substitution", ok, f"method={result['method']} score={result['score']}"


def detector_smoke_test():
    samples = [
        ("Detector Caesar", decrypt_caesar(PLAIN_LONG, 11), "Caesar"),
        ("Detector Atbash", decrypt_atbash(PLAIN_LONG), "Atbash"),
        ("Detector Affine", encrypt_affine(PLAIN_LONG, 7, 3), "Affine"),
        ("Detector Vigenere", encrypt_vigenere(PLAIN_LONG, "FORTIFICATION"), "Vigenere"),
    ]

    passed = 0
    details = []

    for name, ciphertext, expected_word in samples:
        result = detect_cipher(ciphertext)
        combined = " ".join(result["likely_types"] + result["suggestions"])
        ok = expected_word.lower() in combined.lower()
        passed += 1 if ok else 0
        details.append(f"{name}: expected={expected_word}, likely={result['likely_types']}")

    return "Detector smoke test", passed >= 2, f"{passed}/{len(samples)} reasonable predictions | " + " | ".join(details)


def main():
    tests = [
        test_caesar,
        test_atbash,
        test_affine,
        test_vigenere,
        test_beaufort,
        test_rail_fence,
        test_columnar,
        test_rot13,
        test_rot47,
        test_keyword,
        test_playfair,
        test_autokey,
        test_polybius,
        test_baconian,
        test_substitution_atbash_style,
        detector_smoke_test,
    ]

    print()
    print("FreqCrack Ultimate Accuracy Benchmark")
    print("=" * 45)

    passed = 0

    for test in tests:
        name, ok, detail = test()
        passed += 1 if ok else 0
        print(f"{pass_fail(ok):4} | {name:24} | {detail}")

    print("=" * 45)
    print(f"Score: {passed}/{len(tests)} passed")
    print(f"Generated challenge files: {OUT}")
    print()

    if passed == len(tests):
        print("Excellent: all benchmark tests passed.")
    elif passed >= len(tests) - 2:
        print("Good: most tests passed. Review failed cases for detector/scoring improvements.")
    else:
        print("Needs improvement: several solvers or detector rules need tuning.")


if __name__ == "__main__":
    main()
