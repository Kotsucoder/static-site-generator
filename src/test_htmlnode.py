import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestTextNode(unittest.TestCase):
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
    
    def test_parentnode_no_tag(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode(None, [child_node])
        with self.assertRaises(ValueError):
            parent_node.to_html()
    
    def test_parentnode_no_children(self):
        parent_node = ParentNode("br", None)
        with self.assertRaises(ValueError):
            parent_node.to_html()


if __name__ == "__main__":
    unittest.main()