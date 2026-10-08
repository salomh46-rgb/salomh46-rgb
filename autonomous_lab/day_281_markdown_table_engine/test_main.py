import unittest
from main import MarkdownTableEngine

class TestMarkdownTableEngine(unittest.TestCase):
    def test_table_rendering(self):
        headers = ["ID", "Name", "Role"]
        rows = [
            [1, "Jasper", "Architect"],
            [2, "Gemini", "AI Core"]
        ]
        output = MarkdownTableEngine.render(headers, rows)
        self.assertIn("| ID | Name   | Role      |", output)
        self.assertIn("| 1  | Jasper | Architect |", output)

    def test_empty_headers(self):
        self.assertEqual(MarkdownTableEngine.render([], []), "")

if __name__ == "__main__":
    unittest.main()
