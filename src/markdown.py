"""
This module provides functions that manage Markdown text.
"""


from enum import Enum
from re import findall


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
    if markdown_block[0:4] == "```\n" and markdown_block[-4:-1] == "```":
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