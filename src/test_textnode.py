import unittest

from textnode import TextNode, TextType
from main import split_nodes_delimiter, text_node_to_html_node


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
    
    def test_step_delimiter(self):
        test_markdown = "The **quick** brown fox _jumped_ over the `lazy` dog."
        get_bold = split_nodes_delimiter(test_markdown, "**", TextType.BOLD)
        get_italics = split_nodes_delimiter(get_bold, "_", TextType.ITALICS)
        get_codeblock = split_nodes_delimiter(get_italics, "`", TextType.CODEBLOCK)
        html = [text_node_to_html_node(i) for i in get_codeblock]
        formatted_html = [i.to_html() for i in html]
        final_html = ""
        for i in formatted_html:
            final_html += i
        expected_result = "<p>The </p><b>quick</b><p> brown fox </p><i>jumped</i><p> over the </p><code>lazy</code><p> dog.</p>"
        self.assertEqual(final_html, expected_result)


if __name__ == "__main__":
    unittest.main()