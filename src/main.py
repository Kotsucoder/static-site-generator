from textnode import TextType, TextNode
from htmlnode import HTMLNode, LeafNode


def main():
    test_object = TextNode("This is some anchor text", TextType.HYPERLINK,"https://boot.dev")
    print(test_object)

    test_HTML = HTMLNode("a", "Bootdev", None, {"href":"https://boot.dev"})
    print(test_HTML)


def text_node_to_html_node(text_node):
    if type(text_node) is TextNode:
        match(text_node.get_type()):
            case TextType.TEXT:
                return LeafNode("p", text_node.get_text())
            case TextType.BOLD:
                return LeafNode("b", text_node.get_text())
            case TextType.ITALICS:
                return LeafNode("i", text_node.get_text())
            case TextType.CODEBLOCK:
                return LeafNode("code", text_node.get_text())
            case TextType.HYPERLINK:
                return LeafNode("a", text_node.get_text(), {"href":text_node.get_url()})
            case TextType.IMAGE:
                return LeafNode("img", None, {"src":text_node.get_url(), "alt":text_node.get_text()})
            case _:
                raise ValueError("text_node type must be a valid TextType")
    else:
        raise ValueError("text_node must be a TextNode")


if __name__ == "__main__":
    main()