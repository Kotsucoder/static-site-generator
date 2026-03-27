import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_not_eq_text(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is not the same text node", TextType.BOLD)
        self.assertNotEqual(node, node2)
    
    def test_not_eq_type(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.ITALICS)
        self.assertNotEqual(node, node2)

    def test_eq_url(self):
        node = TextNode("Bootdev", TextType.HYPERLINK, "https://boot.dev")
        node2 = TextNode("Bootdev", TextType.HYPERLINK, "https://boot.dev")
        self.assertEqual(node, node2)

    def test_not_eq_url(self):
        node = TextNode("Bootdev", TextType.HYPERLINK, "https://boot.dev")
        node2 = TextNode("Bootdev", TextType.HYPERLINK, "https://www.boot.dev")
        self.assertNotEqual(node, node2)

    def test_none_url(self):
        node = TextNode("Bootdev", TextType.HYPERLINK)
        self.assertIs(node.get_url(), None)
    
    def test_set_url(self):
        node = TextNode("Bootdev", TextType.HYPERLINK, "https://boot.dev")
        self.assertIsInstance(node.get_url(), str)


if __name__ == "__main__":
    unittest.main()