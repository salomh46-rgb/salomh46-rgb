import unittest
from main import BloomFilter

class TestBloomFilter(unittest.TestCase):
    def test_add_and_contains(self):
        bf = BloomFilter(expected_elements=100, false_positive_rate=0.01)
        words = ["apple", "banana", "cherry", "tashkent"]
        for w in words:
            bf.add(w)

        for w in words:
            self.assertTrue(bf.contains(w))

        self.assertFalse(bf.contains("unseen_item_12345"))

    def test_invalid_parameters(self):
        with self.assertRaises(ValueError):
            BloomFilter(expected_elements=0)
        with self.assertRaises(ValueError):
            BloomFilter(false_positive_rate=1.5)

if __name__ == "__main__":
    unittest.main()
