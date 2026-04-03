"""
This module provides functions that manage Markdown text.
"""


from enum import Enum
from re import findall
from htmlnode import LeafNode, ParentNode
from textnode import TextNode, create_textnode_object, text_node_to_html_node


class BlockType(Enum):
    """
    Represents the different types that a Block can be.

    Valid types include:
        BlockType.PARAGRAPH
        BlockType.HEADING
        BlockType.CODE
        BlockType.QUOTE
        BlockType.UNORDERED_LIST
        BlockType.ORDERED_LIST
    """
    PARAGRAPH = "p"
    HEADING = "h"
    CODE = "code"
    QUOTE = "qt"
    UNORDERED_LIST = "ul"
    ORDERED_LIST = "ol"


def markdown_to_blocks(markdown: str) -> list[str]:
    """
    This function converts a full markdown string into a list of blocks.

    Args:
        markdown: Raw markdown text in the form of a String.

    Returns:
        list[str]: Markdown text split into blocks.
    """

    split_markdown = markdown.split("\n\n")
    split_markdown_stripped = [text.strip() for text in split_markdown]
    split_markdown_valid: list[str] = []
    for text in split_markdown_stripped:
        if text:
            split_markdown_valid.append(text)
    return split_markdown_valid


def block_to_block_type(markdown_block: str) -> BlockType:
    """
    Takes in a markdown block and returns the block's type.

    Args:
        markdown_block: A string containing markdown text.
    
    Returns:
        BlockType: The type that cooresponds to the markdown's syntax.
    """

    if markdown_block[0] == "#":
        check = findall(r"^(?!#{7,})#{1,6}", markdown_block)
        if check:
            return BlockType.HEADING
    if markdown_block[0:4] == "```\n" and markdown_block[-3:] == "```":
        return BlockType.CODE
    if markdown_block[0] == ">":
        return BlockType.QUOTE
    line_split = markdown_block.split("\n")
    valid = True
    for line in line_split:
        if line[0:2] != "- ":
            valid = False
            break
    if valid:
        return BlockType.UNORDERED_LIST
    valid = True
    increment = 1
    for line in line_split:
        check = findall(r"^\d+\.\s", line)
        if not check:
            valid = False
            break
        num = int(check[0][:-2])
        if num == increment:
            increment += 1
        else:
            valid = False
            break
    if valid:
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH


def markdown_to_html_node(markdown: str) -> ParentNode:
    markdown_blocks = markdown_to_blocks(markdown)
    primary_parent = ParentNode("div", [])
    for block in markdown_blocks:
        block_st = block.strip()
        check_type = block_to_block_type(block_st)
        match check_type:
            case BlockType.PARAGRAPH:
                leafnodes = create_leafnodes(block)
                primary_parent.children.append(ParentNode("p", leafnodes))
            case BlockType.HEADING:
                octothorpes = findall(r"^(?!#{7,})#{1,6}", block)[0]
                heading_type = len(octothorpes)
                block_h = block[heading_type + 1:]
                leafnodes = create_leafnodes(block_h)
                primary_parent.children.append(ParentNode(f"h{heading_type}", leafnodes))
            case BlockType.CODE:
                node = ParentNode("pre", [LeafNode("code", block.strip()[4:-3])])
                primary_parent.children.append(node)
            case BlockType.QUOTE:
                block_q = block[1:]
                if block_q[0] == " ":
                    block_q = block_q[1:]
                leafnodes = create_leafnodes(block_q)
                primary_parent.children.append(ParentNode("blockquote", leafnodes))
            case BlockType.UNORDERED_LIST:
                ul_parent = ParentNode("ul", [])
                lines = block.split("\n")
                for line in lines:
                    leafnodes = create_leafnodes(line[2:])
                    ul_parent.children.append(ParentNode("li", leafnodes))
                primary_parent.children.append(ul_parent)
            case BlockType.ORDERED_LIST:
                ol_parent = ParentNode("ol", [])
                lines = block.split("\n")
                for line in lines:
                    leafnodes = create_leafnodes(line[3:])
                    ol_parent.children.append(ParentNode("li", leafnodes))
                primary_parent.children.append(ol_parent)
    return primary_parent


def create_leafnodes(markdown: str) -> list[LeafNode]:
    markdown_nl = markdown.replace("\n", " ")
    textnodes = create_textnode_object(markdown_nl)
    leafnodes = []
    for textnode in textnodes:
        leafnodes.append(text_node_to_html_node(textnode))
    return leafnodes

if __name__ == "__main__":
    md = """
- One
- Two
- Three
- Four **Bolded** Queens
- Five _Italic_ Kings
"""
    node = markdown_to_html_node(md)
    html = node.to_html()