import unittest
from markdown_blocks import (
    markdown_to_blocks, 
    block_to_block_type,
    BlockType,
    markdown_to_html_node
)

class TestMarkdown(unittest.TestCase):

    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
        """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )


    def test_markdown_to_blocks_with_extra_spaces(self):
        md = """


This is **bolded** paragraph


This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line



- This is a list
- with items
        """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_blocks_paragraph(self):
        md = "This is a normal paragraph"
        block_type = block_to_block_type(md)
        self.assertEqual(block_type, BlockType.PARAGRAPH)

    def test_blocks_heading(self):
        md = "#HEADER 1"
        block_type = block_to_block_type(md)
        self.assertEqual(block_type, BlockType.HEADING)

    def test_blocks_code(self):
        md = "```\nThis is a code paragraph\n```"
        block_type = block_to_block_type(md)
        self.assertEqual(block_type, BlockType.CODE)

    def test_WRONG_blocks_code(self):
        md = "```\nThis is a code paragraph\n``"
        block_type = block_to_block_type(md)
        self.assertEqual(block_type, BlockType.PARAGRAPH)

    def test_blocks_quote(self):
        md = ">Cogito ergo sum"
        block_type = block_to_block_type(md)
        self.assertEqual(block_type, BlockType.QUOTE)

    def test_WRONG_blocks_quote(self):
        md = ">Cogito ergo sum\n>Alea iacta est\nMa io che cazzo ne so"
        block_type = block_to_block_type(md)
        self.assertEqual(block_type, BlockType.PARAGRAPH)

    def test_blocks_unordered_list(self):
        md = "- item \n- another item 2\n- one more item"
        block_type = block_to_block_type(md)
        self.assertEqual(block_type, BlockType.UNORDERED_LIST)

    def test_WRONG_blocks_unordered_list(self):
        md = "- item \n- another item 2\n- one more item\nfanculo gli elenchi"
        block_type = block_to_block_type(md)
        self.assertEqual(block_type, BlockType.PARAGRAPH)

    def test_blocks_ordered_list(self):
        md = "1. item one\n2. item two\n3. item three"
        block_type = block_to_block_type(md)
        self.assertEqual(block_type, BlockType.ORDERED_LIST)

    def test_WRONG_blocks_ordered_list(self):
        md = "1. item one\n2. item two\n3. item three\nD. item dee"
        block_type = block_to_block_type(md)
        self.assertEqual(block_type, BlockType.PARAGRAPH)

    def test_paragraphs(self):
            md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""
            node = markdown_to_html_node(md)
            html = node.to_html()
            self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
            )


    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )


    def test_headings_and_paragraph(self):
        md = """
# This is a _very_ cool heading

This is a paragraph

## Second heading
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>This is a <i>very</i> cool heading</h1><p>This is a paragraph</p><h2>Second heading</h2></div>",
        )


    def test_ordered_list(self):
        md = """
1. item one
2. **important** item
3. item
4. item
5. item
6. item
7. item
8. item
9. item
10. item
11. item
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>item one</li><li><b>important</b> item</li><li>item</li><li>item</li><li>item</li><li>item</li><li>item</li><li>item</li><li>item</li><li>item</li><li>item</li></ol></div>",
        )

    def test_unordered_list(self):
        md = """
- item one
- **important** item
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>item one</li><li><b>important</b> item</li></ul></div>",
        )

    def test_images_and_links(self):
        md = """
This is a paragraph with a [link](https://www.google.com).

And here we have a photo ![Description of image](url/of/image.jpg)
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            '<div><p>This is a paragraph with a <a href="https://www.google.com">link</a>.</p><p>And here we have a photo <img src="url/of/image.jpg" alt="Description of image"></img></p></div>'
        )