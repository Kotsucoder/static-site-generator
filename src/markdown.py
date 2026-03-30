"""
This module provides functions that manage Markdown text.
"""


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