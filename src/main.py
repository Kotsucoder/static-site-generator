from textnode import TextType, TextNode, split_nodes_delimiter, text_node_to_html_node
from htmlnode import HTMLNode, LeafNode


def main() -> None:
    """
    Main entry point for the program.
    """
    test_markdown = [TextNode("The **quick** brown fox _jumped_ over the `lazy` dog.", TextType.TEXT)]
    get_bold = split_nodes_delimiter(test_markdown, "**", TextType.BOLD)
    get_italics = split_nodes_delimiter(get_bold, "_", TextType.ITALICS)
    get_codeblock = split_nodes_delimiter(get_italics, "`", TextType.CODEBLOCK)
    html = [text_node_to_html_node(i) for i in get_codeblock]
    formatted_html = [i.to_html() for i in html]
    final_html = ""
    for i in formatted_html:
        final_html += i
    print(final_html)


if __name__ == "__main__":
    main()