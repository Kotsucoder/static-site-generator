from textnode import TextType, TextNode


def main():
    test_object = TextNode("This is some anchor text", TextType.HYPERLINK,"https://boot.dev")
    print(test_object)


if __name__ == "__main__":
    main()