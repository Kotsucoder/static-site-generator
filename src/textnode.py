"""
This module provides objects that should be used for representing and working with Markdown syntax
parsing. These objects provide a semantic representation of the syntax to make it easier to manage
the raw text in a clear, defined data structure.

Classes:
    TextType: Represents the different types that a TextNode can represent.
    TextNode: Data structure which semantically represents Markdown syntax into objects.

Functions:
    split_node_delimiter: Splits TextNodes by a delimiter.
    text_node_to_html_node: Converts TextNode objects to LeafNode objects.
    extract_markdown_images: Extracts markdown images from string.
    extract_markdown_links: Extracts markdown hyperlinks from string.
    split_nodes_image: Splits TextNodes, separating images from the text.
    split_nodes_hyperlink: Splits TextNodes, separating hyperlinks from the text.
    create_textnode_object: Generates TextNode objects from a given markdown string.
"""


from enum import Enum
from typing import Optional
from htmlnode import LeafNode
from re import findall


class TextType(Enum):
    """
    Represents the different types that a TextNode can represent.

    Valid types include:
        TextType.TEXT
        TextType.BOLD
        TextType.ITALICS
        TextType.CODEBLOCK
        TextType.HYPERLINK
        TextType.IMAGE
    """
    TEXT = "text"
    BOLD = "bold"
    ITALICS = "italics"
    CODEBLOCK = "code"
    HYPERLINK = "link"
    IMAGE = "image"


class TextNode:
    """
    Data structure which semantically represents Markdown syntax into objects.

    Attributes:
        text: String representing the TextNode's contents.
        text_type: TextType object defining the type of this node.
        url: Optional string representing the url that may be attached to the node.
    """

    def __init__(self, text: str, text_type: TextType, url:Optional[str]=None) -> None:
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other: object) -> bool:
        if type(other) is TextNode:
            sametext = self.text == other.text
            sametype = self.text_type == other.text_type
            sameurl = self.url == other.url
        else:
            return NotImplemented
        return sametext and sametype and sameurl
    
    def __repr__(self) -> str:
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"


def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
    """
    Splits TextNodes by a delimiter.

    Args:
        old_nodes: A list of TextNode objects.
        delimiter: A string that is used to split the TextNode.
        text_type: The TextType object representing the TextNode type that is split from the main text.

    Returns:
        list[TextNode]: The list of TextNode objects split by the delimiter.
    """

    new_nodes = []
    for node in old_nodes:
        if node.text_type is not TextType.TEXT:
            new_nodes.append(node)
        else:
            split_node = node.text.split(delimiter)
            text_node = True
            types = {True: TextType.TEXT, False: text_type}
            for new_node in split_node:
                if new_node:
                    create_node = TextNode(new_node, types[text_node])
                    new_nodes.append(create_node)
                text_node = not text_node
    if node.text_type is not TextType.TEXT:
        raise ValueError("delimiter must come in pairs.")
    return new_nodes


def text_node_to_html_node(text_node: TextNode) -> LeafNode:
    """
    Converts TextNode objects to LeafNode objects.

    Args:
        text_node: A TextNode object representing a Markdown segment.
    
    Returns:
        LeafNode: A LeafNode object representing a HTML element derived from the Markdown.
    
    Raises:
        TypeError: text_node type must be a valid TextType
    """

    match(text_node.text_type):
        case TextType.TEXT:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALICS:
            return LeafNode("i", text_node.text)
        case TextType.CODEBLOCK:
            return LeafNode("code", text_node.text)
        case TextType.HYPERLINK:
            if text_node.url is None:
                raise ValueError("Hyperlinks must contain a URL.")
            return LeafNode("a", text_node.text, {"href":text_node.url})
        case TextType.IMAGE:
            if text_node.url is None:
                raise ValueError("Image objects must contain a URL.")
            return LeafNode("img", None, {"src":text_node.url, "alt":text_node.text})
        case _:
            raise TypeError("text_node type must be a valid TextType")


def extract_markdown_images(text: str) -> list[tuple[str,str]]:
    """
    Extracts markdown images from string.

    Args:
        text: The raw markdownstring to extract the images from.
    
    Returns:
        list[tuple]: A list of tuples in the form (alt_text, url).
    """

    images: list[tuple[str,str]] = findall(r"!\[(.*?)\]\((.*?)\)", text)
    return images


def extract_markdown_links(text: str) -> list[tuple[str,str]]:
    """
    Extracts markdown hyperlinks from string.

    Args:
        text: The raw markdownstring to extract the hyperlink from.
    
    Returns:
        list[tuple]: A list of tuples in the form (text, url).
    """

    links: list[tuple[str,str]] = findall(r"(?<!!)\[(.*?)\]\((.*?)\)", text)
    return links


def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    """
    Splits TextNodes, separating images from the text.

    Args:
        old_nodes: A list of TextNode objects.
    
    Returns:
        list[TextNode]: The list of TextNode objects with the image part separated.
    """

    new_nodes = []
    for node in old_nodes:
        if node.text_type is not TextType.TEXT:
            new_nodes.append(node)
        else:
            delimiters = extract_markdown_images(node.text)
            working_text = node.text
            for delimiter in delimiters:
                delimiter_str = f"![{delimiter[0]}]({delimiter[1]})"
                split_node = working_text.split(delimiter_str)
                new_nodes.append(TextNode(split_node[0], TextType.TEXT))
                new_nodes.append(TextNode(delimiter[0], TextType.IMAGE, delimiter[1]))
                working_text = split_node[1]
            if working_text:
                new_nodes.append(TextNode(working_text, TextType.TEXT))
    return new_nodes


def split_nodes_hyperlink(old_nodes: list[TextNode]) -> list[TextNode]:
    """
    Splits TextNodes, separating hyperlinks from the text.

    Args:
        old_nodes: A list of TextNode objects.
    
    Returns:
        list[TextNode]: The list of TextNode objects with the hyperlink part separated.
    """

    new_nodes = []
    for node in old_nodes:
        if node.text_type is not TextType.TEXT:
            new_nodes.append(node)
        else:
            delimiters = extract_markdown_links(node.text)
            working_text = node.text
            for delimiter in delimiters:
                delimiter_str = f"[{delimiter[0]}]({delimiter[1]})"
                split_node = working_text.split(delimiter_str)
                new_nodes.append(TextNode(split_node[0], TextType.TEXT))
                new_nodes.append(TextNode(delimiter[0], TextType.HYPERLINK, delimiter[1]))
                working_text = split_node[1]
            if working_text:
                new_nodes.append(TextNode(working_text, TextType.TEXT))
    return new_nodes


def create_textnode_object(text: str) -> list[TextNode]:
    """
    Generates TextNode objects from a given markdown string.

    Args:
        text: The markdown string to convert to TextNode objects.

    Returns:
        list[TextNode]: Generated List of TextNode objects.
    """

    initial_textnode = [TextNode(text, TextType.TEXT)]
    bold_text = split_nodes_delimiter(initial_textnode, "**", TextType.BOLD)
    italic_text = split_nodes_delimiter(bold_text, "_", TextType.ITALICS)
    code_block = split_nodes_delimiter(italic_text, "`", TextType.CODEBLOCK)
    links = split_nodes_hyperlink(code_block)
    images = split_nodes_image(links)
    return images