import unittest
from markdown import *


class TestMarkdown(unittest.TestCase):
    def test_markdown_split(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        expected_result = [
            "This is **bolded** paragraph",
            "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
            "- This is a list\n- with items"
        ]
        self.assertEqual(blocks, expected_result)

    def test_markdown_paragraph_type(self):
        md_block = "Hello, World!"
        md_type = block_to_block_type(md_block)
        self.assertEqual(md_type, BlockType.PARAGRAPH)
    
    def test_markdown_heading_type(self):
        md_block = "### Heading 3"
        md_type = block_to_block_type(md_block)
        self.assertEqual(md_type, BlockType.HEADING)
    
    def test_markdown_heading_extra_type(self):
        md_block = "####### Not a valid heading"
        md_type = block_to_block_type(md_block)
        self.assertEqual(md_type, BlockType.PARAGRAPH)
    
    def test_markdown_code_type(self):
        md_block = """```
Test block
```
"""
        md_type = block_to_block_type(md_block)
        self.assertEqual(md_type, BlockType.CODE)
    
    def test_markdown_quote_type(self):
        md_block = "> Failure is the path to success"
        md_type = block_to_block_type(md_block)
        self.assertEqual(md_type, BlockType.QUOTE)
    
    def test_markdown_ul_type(self):
        md_block = """- One
- Two
- Three"""
        md_type = block_to_block_type(md_block)
        self.assertEqual(md_type, BlockType.UNORDERED_LIST)
    
    def test_markdown_ol_type(self):
        md_block = """1. One
2. Two
3. Three"""
        md_type = block_to_block_type(md_block)
        self.assertEqual(md_type, BlockType.ORDERED_LIST)
    
    def test_markdown_ol_fail_type(self):
        md_block = """1. One
3. Three
5. Five"""
        md_type = block_to_block_type(md_block)
        self.assertEqual(md_type, BlockType.PARAGRAPH)


if __name__ == "__main__":
    unittest.main()