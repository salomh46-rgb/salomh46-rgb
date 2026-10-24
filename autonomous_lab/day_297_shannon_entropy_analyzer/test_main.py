import unittest
from main import ShannonEntropyAnalyzer

class TestShannonEntropyAnalyzer(unittest.TestCase):
    def test_low_entropy(self):
        res = ShannonEntropyAnalyzer.evaluate_strength("aaaaaa")
        self.assertEqual(res["rating"], "VERY_WEAK")
        self.assertFalse(res["is_secure"])

    def test_high_entropy_crypto_token(self):
        # 64 character hex string
        token = "9f83c605d84a32a688b776f87424ad419e7cf887cf479426f4f5a3598e0409a2"
        res = ShannonEntropyAnalyzer.evaluate_strength(token)
        self.assertIn(res["rating"], ["STRONG", "CRYPTOGRAPHIC_GRADE"])
        self.assertTrue(res["is_secure"])

if __name__ == "__main__":
    unittest.main()
