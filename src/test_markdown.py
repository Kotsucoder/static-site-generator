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
```"""
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
    
    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        expected_value = "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>"
        self.assertEqual(html, expected_value)
    
    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        expected_value = "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>"
        self.assertEqual(html, expected_value)
    
    def test_heading(self):
        md = """
### Heading 3 **bold** Heading
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        expected_value = "<div><h3>Heading 3 <b>bold</b> Heading</h3></div>"
        self.assertEqual(html, expected_value)
    
    def test_quote(self):
        md = """
> Failure is the path to success
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        expected_value = "<div><blockquote>Failure is the path to success</blockquote></div>"
        self.assertEqual(html, expected_value)
    
    def test_unordered_list(self):
        md = """
- One
- Two
- Three
- Four **Bolded** Queens
- Five _Italic_ Kings
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        expected_value = "<div><ul><li>One</li><li>Two</li><li>Three</li><li>Four <b>Bolded</b> Queens</li><li>Five <i>Italic</i> Kings</li></ul></div>"
        self.assertEqual(html, expected_value)
    
    def test_ordered_list(self):
        md = """
1. One
2. Two
3. Three
4. Four **Bolded** Queens
5. Five _Italic_ Kings
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        expected_value = "<div><ol><li>One</li><li>Two</li><li>Three</li><li>Four <b>Bolded</b> Queens</li><li>Five <i>Italic</i> Kings</li></ol></div>"
        self.assertEqual(html, expected_value)


if __name__ == "__main__":
    unittest.main()