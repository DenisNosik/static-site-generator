import unittest

from split_nodes import split_nodes_delimiter
from textnode import TextNode, TextType


class TestSplitNodes(unittest.TestCase):
    def test_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes, [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ])
    
    def test_bold(self):
        node = TextNode("This is a **VERY BOLD** Text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(new_nodes, [
            TextNode("This is a ", TextType.TEXT),
            TextNode("VERY BOLD", TextType.BOLD),
            TextNode(" Text", TextType.TEXT),
        ])
    
    def test_double_bold(self):
        node = TextNode("This is a **VERY BOLD** Text like **THIS ONE**", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(new_nodes, [
            TextNode("This is a ", TextType.TEXT),
            TextNode("VERY BOLD", TextType.BOLD),
            TextNode(" Text like ", TextType.TEXT),
            TextNode("THIS ONE", TextType.BOLD),
        ])
    
    def test_bold_and_italic(self):
        node = TextNode("**VERY BOLD** Text and _very italic one_", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
        self.assertEqual(new_nodes, [
            TextNode("VERY BOLD", TextType.BOLD),
            TextNode(" Text and ", TextType.TEXT),
            TextNode("very italic one", TextType.ITALIC),
        ])