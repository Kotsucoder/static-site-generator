from textnode import TextType, TextNode
from htmlnode import HTMLNode


def main():
    test_object = TextNode("This is some anchor text", TextType.HYPERLINK,"https://boot.dev")
    print(test_object)

    test_HTML = HTMLNode("a", "Bootdev", None, {"href":"https://boot.dev"})
    print(test_HTML)


if __name__ == "__main__":
    main()