from textnode import TextType, TextNode
from htmlnode import HTMLNode, LeafNode


def main():
    test_markdown = "The **quick** brown fox _jumped_ over the `lazy` dog."
    get_bold = split_nodes_delimiter(test_markdown, "**", TextType.BOLD)
    get_italics = split_nodes_delimiter(get_bold, "_", TextType.ITALICS)
    get_codeblock = split_nodes_delimiter(get_italics, "`", TextType.CODEBLOCK)
    html = [text_node_to_html_node(i) for i in get_codeblock]
    formatted_html = [i.to_html() for i in html]
    final_html = ""
    for i in formatted_html:
        final_html += i
    print(final_html)


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

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    if type(old_nodes) is not list:
        first_node = TextNode(old_nodes, TextType.TEXT)
        old_nodes = [first_node]
    new_nodes = []
    for node in old_nodes:
        if node.get_type() is not TextType.TEXT:
            new_nodes.append(node)
        else:
            split_node = node.get_text().split(delimiter)
            text_node = True
            types = {True: TextType.TEXT, False: text_type}
            for new_node in split_node:
                if new_node:
                    create_node = TextNode(new_node, types[text_node])
                    new_nodes.append(create_node)
                text_node = not text_node
    return new_nodes


if __name__ == "__main__":
    main()