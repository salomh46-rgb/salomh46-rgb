import unittest
from main import TelegramSanitizer

class TestTelegramSanitizer(unittest.TestCase):
    def test_escape_special_chars(self):
        raw = "Hello! Price: $50.00. Status: [PENDING] (v1.2.0)"
        escaped = TelegramSanitizer.escape_markdown_v2(raw)
        self.assertIn(r"Hello\!", escaped)
        self.assertIn(r"50\.00", escaped)
        self.assertIn(r"\[PENDING\]", escaped)

    def test_code_block_formatting(self):
        code = 'x = 10; print(f"val: {x}")'
        formatted = TelegramSanitizer.format_code_block(code, "python")
        self.assertTrue(formatted.startswith("```python"))
        self.assertTrue(formatted.endswith("```"))

if __name__ == "__main__":
    unittest.main()
