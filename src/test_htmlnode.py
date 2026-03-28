import unittest

from textnode import TextNode, TextType, text_node_to_html_node
from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_formatting_a(self):
        node = HTMLNode("a", "Bootdev", None, {"href":"https://boot.dev"})
        node2 = "HTMLNode(a, Bootdev, None, {'href': 'https://boot.dev'})"
        self.assertEqual(str(node), node2)

    def test_formatting_p(self):
        node = HTMLNode("p", "This should work just fine")
        node2 = "HTMLNode(p, This should work just fine, None, None)"
        self.assertEqual(str(node), node2)
    
    def test_formatting_br(self):
        node = HTMLNode("br")
        node2 = "HTMLNode(br, None, None, None)"
        self.assertEqual(str(node), node2)
    
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        node2 = "<p>Hello, world!</p>"
        self.assertEqual(node.to_html(), node2)
    
    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Bootdev", {"href":"https://boot.dev"})
        node2 = "<a href=\"https://boot.dev\">Bootdev</a>"
        self.assertEqual(node.to_html(), node2)
    
    def test_leaf_to_html_br(self):
        node = LeafNode("br", None)
        with self.assertRaises(ValueError):
            node.to_html()
    
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )
    
    def test_text_node_to_paragraph(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "p")
        self.assertEqual(html_node.value, "This is a text node")
    
    def test_text_node_to_bold(self):
        node = TextNode("This is a text node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a text node")
    
    def test_text_node_to_italics(self):
        node = TextNode("This is a text node", TextType.ITALICS)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is a text node")
    
    def test_text_node_to_code(self):
        node = TextNode("print(\"Hello, World!\")", TextType.CODEBLOCK)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "print(\"Hello, World!\")")
    
    def test_text_node_to_hyperlink(self):
        node = TextNode("Bootdev", TextType.HYPERLINK, "https://boot.dev")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "Bootdev")
        self.assertEqual(html_node.props, {"href":"https://boot.dev"})
    
    def test_text_node_to_image(self):
        node = TextNode("Catdog", TextType.IMAGE, "/assets/catdog.png")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, None)
        self.assertEqual(html_node.props, {"src":"/assets/catdog.png","alt":"Catdog"})


if __name__ == "__main__":
    unittest.main()