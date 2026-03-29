import unittest
from textnode import *


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
        self.assertIs(node.url, None)
    
    def test_set_url(self):
        node = TextNode("Bootdev", TextType.HYPERLINK, "https://boot.dev")
        self.assertIsInstance(node.url, str)
    
    def test_step_delimiter(self):
        test_markdown = [TextNode("The **quick** brown fox _jumped_ over the `lazy` dog.", TextType.TEXT)]
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
    
    def test_image_extraction(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        matches = extract_markdown_images(text)
        self.assertListEqual([("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")], matches)
    
    def test_link_extraction(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        matches = extract_markdown_links(text)
        self.assertListEqual([("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")], matches)
    
    def test_image_split(self):
        text = "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)"
        text_node = [TextNode(text, TextType.TEXT)]
        new_text = split_nodes_image(text_node)
        expected_result = [
            TextNode("This is text with an ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(" and another ", TextType.TEXT),
            TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png")
        ]
        self.assertEqual(new_text, expected_result)

    def test_hyperlink_split(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        text_node = [TextNode(text, TextType.TEXT)]
        new_text = split_nodes_hyperlink(text_node)
        expected_result = [
            TextNode("This is text with a link ", TextType.TEXT),
            TextNode("to boot dev", TextType.HYPERLINK, "https://www.boot.dev"),
            TextNode(" and ", TextType.TEXT),
            TextNode("to youtube", TextType.HYPERLINK, "https://www.youtube.com/@bootdotdev")
        ]
        self.assertEqual(new_text, expected_result)

if __name__ == "__main__":
    unittest.main()