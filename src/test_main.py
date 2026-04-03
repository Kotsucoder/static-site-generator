import unittest
from main import *


class TestMarkdown(unittest.TestCase):
    def test_title(self):
        md = "# Small Burst of Imagination"
        title = extract_title(md)
        expected_result = "Small Burst of Imagination"
        self.assertEqual(title, expected_result)

    def test_not_a_title(self):
        md = "## Not a title"
        try:
            title = extract_title(md)
        except ValueError:
            title = None
        self.assertEqual(title, None)


if __name__ == "__main__":
    unittest.main()