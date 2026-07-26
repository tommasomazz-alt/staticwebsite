import unittest
from textnode import TextNode, TextType, text_node_to_html_node
from inline_functions import split_nodes_delimiter

class TestSplitNodes(unittest.TestCase):
    def test_basic(self):
        nodes_list = [
            TextNode("This is a **bold** word", TextType.TEXT),
        ]
        split_test = split_nodes_delimiter(nodes_list,"**",TextType.BOLD)
        expected_result = [
            TextNode("This is a ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" word", TextType.TEXT),

        ]
        self.assertEqual(split_test, expected_result)
    
    def test_multiple_bold(self):
        nodes_list = [
            TextNode("This is a **bold** word and **this one** too", TextType.TEXT),
        ]
        split_test = split_nodes_delimiter(nodes_list,"**",TextType.BOLD)
        expected_result = [
            TextNode("This is a ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" word and ", TextType.TEXT),
            TextNode("this one", TextType.BOLD),
            TextNode(" too", TextType.TEXT),

        ]
        self.assertEqual(split_test, expected_result)

    def test_multiple_italic(self):
        nodes_list = [
            TextNode("This is a _italic_ word and _this one_ too", TextType.TEXT),
        ]
        split_test = split_nodes_delimiter(nodes_list,"_",TextType.ITALIC)
        expected_result = [
            TextNode("This is a ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and ", TextType.TEXT),
            TextNode("this one", TextType.ITALIC),
            TextNode(" too", TextType.TEXT),

        ]
        self.assertEqual(split_test, expected_result)
    
    def test_multiple_code(self):
        nodes_list = [
            TextNode("This is a `code` piece and `this one` too", TextType.TEXT),
        ]
        split_test = split_nodes_delimiter(nodes_list,"`",TextType.CODE)
        expected_result = [
            TextNode("This is a ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" piece and ", TextType.TEXT),
            TextNode("this one", TextType.CODE),
            TextNode(" too", TextType.TEXT),

        ]
        self.assertEqual(split_test, expected_result)

    def test_starting_delimiter(self):
        nodes_list = [
            TextNode("**This is a bold** section", TextType.TEXT),
        ]
        split_test = split_nodes_delimiter(nodes_list,"**",TextType.BOLD)
        expected_result = [
            TextNode("This is a bold", TextType.BOLD),
            TextNode(" section", TextType.TEXT),

        ]
        self.assertEqual(split_test, expected_result)

    def test_multiple_node_types(self):
        nodes_list = [
            TextNode("**This is a bold** section", TextType.TEXT),
            TextNode("This is a _italic_ word", TextType.TEXT),
            TextNode("bold words", TextType.BOLD),

        ]
        split_test = split_nodes_delimiter(nodes_list,"**",TextType.BOLD)
        expected_result = [
            TextNode("This is a bold", TextType.BOLD),
            TextNode(" section", TextType.TEXT),
            TextNode("This is a _italic_ word", TextType.TEXT),
            TextNode("bold words", TextType.BOLD),

        ]
        self.assertEqual(split_test, expected_result)

    def test_missing_delimiter(self):
        nodes_list = [
            TextNode("**This is a wrong bold section", TextType.TEXT),
        ]

        with self.assertRaises(Exception):
            split_test = split_nodes_delimiter(nodes_list,"**",TextType.BOLD)