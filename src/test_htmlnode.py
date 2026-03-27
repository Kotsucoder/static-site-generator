import unittest

from htmlnode import HTMLNode


class TestTextNode(unittest.TestCase):
    def test_formatting_a(self):
        node = HTMLNode("a", "Bootdev", None, {"href":"https://boot.dev"})
        node2 = "<a href=\"https://boot.dev\">Bootdev</a>"
        self.assertEqual(str(node), node2)

    def test_formatting_p(self):
        node = HTMLNode("p", "This should work just fine")
        node2 = "<p>This should work just fine</p>"
        self.assertEqual(str(node), node2)
    
    def test_formatting_br(self):
        node = HTMLNode("br")
        node2 = "<br>"
        self.assertEqual(str(node), node2)


if __name__ == "__main__":
    unittest.main()