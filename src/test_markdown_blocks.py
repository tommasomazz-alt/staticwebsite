import unittest
from markdown_blocks import (
    markdown_to_blocks, 
    block_to_block_type,
    BlockType
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