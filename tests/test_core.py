import unittest

from freqcrack.core.text import clean_text
from freqcrack.core.frequency import letter_frequency, ngram_frequency, index_of_coincidence
from freqcrack.core.caesar import decrypt_caesar, crack_caesar
from freqcrack.core.atbash import decrypt_atbash
from freqcrack.core.affine import decrypt_affine, crack_affine
from freqcrack.core.vigenere import encrypt_vigenere, decrypt_vigenere, crack_vigenere
from freqcrack.core.beaufort import encrypt_beaufort, decrypt_beaufort, crack_beaufort
from freqcrack.core.railfence import encrypt_rail_fence, decrypt_rail_fence, crack_rail_fence
from freqcrack.core.columnar import encrypt_columnar, decrypt_columnar, crack_columnar
from freqcrack.core.substitution import crack_substitution_hillclimb
from freqcrack.core.rot import decrypt_rot, decrypt_rot47
from freqcrack.core.keyword import encrypt_keyword, decrypt_keyword
from freqcrack.core.playfair import encrypt_playfair, decrypt_playfair


class TestCoreTools(unittest.TestCase):
    def test_clean_text(self):
        self.assertEqual(clean_text("Hello, World! 123"), "HELLOWORLD")

    def test_frequency_tools(self):
        freqs = letter_frequency("AABBC")
        self.assertEqual(freqs["A"], 40.0)
        self.assertEqual(freqs["B"], 40.0)
        self.assertEqual(freqs["C"], 20.0)

        self.assertEqual(ngram_frequency("ABABAB", 2, 2)[0], ("AB", 3))
        self.assertGreater(index_of_coincidence("HELLOWORLDHELLOWORLD"), 0)

    def test_caesar(self):
        plaintext = "HELLO WORLD THIS IS A TEST MESSAGE FOR FREQCRACK"
        ciphertext = "KHOOR ZRUOG WKLV LV D WHVW PHVVDJH IRU IUHTFUDFN"

        self.assertEqual(decrypt_caesar(ciphertext, 3), plaintext)
        self.assertEqual(crack_caesar(ciphertext, top=1)[0]["plaintext"].strip(), plaintext)

    def test_atbash(self):
        ciphertext = "SVOOL DLIOW GSRH RH Z GVHG NVHHZTV ULI UIVJXIZXP"
        plaintext = "HELLO WORLD THIS IS A TEST MESSAGE FOR FREQCRACK"

        self.assertEqual(decrypt_atbash(ciphertext), plaintext)

    def test_affine(self):
        ciphertext = "RCLLA OAPLX ZRWU WU I ZCUZ QCUUIMC HAP HPCKSPISG"
        plaintext = "HELLO WORLD THIS IS A TEST MESSAGE FOR FREQCRACK"

        self.assertEqual(decrypt_affine(ciphertext, 5, 8), plaintext)
        self.assertEqual(crack_affine(ciphertext, top=1)[0]["plaintext"].strip(), plaintext)

    def test_vigenere(self):
        plaintext = (
            "HELLO WORLD THIS IS A TEST MESSAGE FOR FREQCRACK. "
            "THIS TOOL CAN ANALYZE LETTER FREQUENCY AND HELP SOLVE CLASSICAL CIPHERS."
        )
        key = "LEMON"
        ciphertext = encrypt_vigenere(plaintext, key)

        self.assertEqual(decrypt_vigenere(ciphertext, key), plaintext)
        self.assertEqual(crack_vigenere(ciphertext, max_key_length=6, top=1)[0]["key"], key)

    def test_beaufort(self):
        plaintext = (
            "HELLO WORLD THIS IS A TEST MESSAGE FOR FREQCRACK. "
            "THIS TOOL CAN ANALYZE LETTER FREQUENCY AND HELP SOLVE CLASSICAL CIPHERS."
        )
        key = "LEMON"
        ciphertext = encrypt_beaufort(plaintext, key)

        self.assertEqual(decrypt_beaufort(ciphertext, key), plaintext)
        self.assertEqual(crack_beaufort(ciphertext, max_key_length=6, top=1)[0]["key"], key)

    def test_rail_fence(self):
        plaintext = "HELLOWORLDTHISISATESTMESSAGEFORFREQCRACK"
        ciphertext = encrypt_rail_fence(plaintext, 3)

        self.assertEqual(decrypt_rail_fence(ciphertext, 3), plaintext)
        self.assertEqual(crack_rail_fence(ciphertext, max_rails=6, top=1)[0]["plaintext"], plaintext)

    def test_columnar(self):
        plaintext = "HELLOWORLDTHISISATESTMESSAGEFORFREQCRACK"
        order = [2, 0, 4, 1, 5, 3]
        ciphertext = encrypt_columnar(plaintext, order)

        self.assertEqual(decrypt_columnar(ciphertext, order), plaintext)
        self.assertEqual(crack_columnar(ciphertext, max_columns=6, top=1)[0]["plaintext"], plaintext)

    def test_keyword(self):
        plaintext = "HELLO WORLD THIS IS A TEST MESSAGE FOR FREQCRACK"
        key = "CIPHER"

        ciphertext = encrypt_keyword(plaintext, key)
        self.assertEqual(decrypt_keyword(ciphertext, key), plaintext)

    def test_playfair(self):
        plaintext = "HIDE THE GOLD IN THE TREE STUMP"
        key = "PLAYFAIR EXAMPLE"

        ciphertext = encrypt_playfair(plaintext, key)
        self.assertEqual(ciphertext, "BMODZBXDNABEKUDMUIXMMOUVIF")
        self.assertEqual(decrypt_playfair(ciphertext, key), "HIDETHEGOLDINTHETREXESTUMP")

    def test_rot(self):
        plaintext = "HELLO WORLD THIS IS A TEST MESSAGE FOR FREQCRACK"

        rot13 = decrypt_rot(plaintext, 13)
        self.assertEqual(decrypt_rot(rot13, 13), plaintext)

        rot47 = decrypt_rot47(plaintext)
        self.assertEqual(decrypt_rot47(rot47), plaintext)

    def test_substitution_advanced(self):
        ciphertext = "SVOOL DLIOW GSRH RH Z GVHG NVHHZTV ULI UIVJXIZXP"
        plaintext = "HELLO WORLD THIS IS A TEST MESSAGE FOR FREQCRACK"

        result = crack_substitution_hillclimb(
            ciphertext,
            restarts=0,
            iterations=0,
            seed=1337,
        )

        self.assertEqual(result["plaintext"].strip(), plaintext)


if __name__ == "__main__":
    unittest.main()
