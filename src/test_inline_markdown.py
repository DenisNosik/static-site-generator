import unittest
from textnode import TextNode, TextType
from inline_markdown import (
    split_nodes_delimiter, extract_markdown_links, 
    extract_markdown_images, split_nodes_image, split_nodes_link,
    text_to_textnodes
    )



class TestTextToTextNodes(unittest.TestCase):
    def test_eq(self):
        text = (
            "This is just a **BOLD** and this is an _italic_ one! very ![cool image](/imgs/cool.jpg) isn't it? and this [link](https://somesome.some) too!"
            )
        nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("This is just a ", TextType.TEXT),
                TextNode("BOLD", TextType.BOLD),
                TextNode(" and this is an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" one! very ", TextType.TEXT),
                TextNode("cool image", TextType.IMAGE, "/imgs/cool.jpg"),
                TextNode(" isn't it? and this ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://somesome.some"),
                TextNode(" too!", TextType.TEXT),
            ],
            nodes
        )
    
    def test_just_text(self):
        text = (
            "This is just a text"
            )
        nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("This is just a text", TextType.TEXT),
            ],
            nodes
        )
    

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

class TestExtractMarkdown(unittest.TestCase):
    def test_images(self):
        matches = extract_markdown_images(
            "This is a text with an ![image](/public/cool_image.jpg)"
        )
        self.assertEqual(matches, [("image", "/public/cool_image.jpg")])
    
    def test_links(self):
        matches = extract_markdown_links(
            "This is text with a link [CLICK ME!](https://somesome.some) and [CLICK ME 2!](https://www.somesome2.some)"
        )
        self.assertEqual(matches, [("CLICK ME!", "https://somesome.some"), ("CLICK ME 2!", "https://www.somesome2.some")])

class TestSplitNodesImageLink(unittest.TestCase):
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
            ],
            new_nodes,
        )
    
    def test_split_links(self):
        node = TextNode(
            "This is text with a [Link!](https://somesome.some) and another [Link2!](https://somesome2.some)"
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("Link!", TextType.LINK, "https://somesome.some"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("Link2!", TextType.LINK, "https://somesome2.some"),
            ],
            new_nodes,
        )
    
    def test_split_images_multy(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        node2 = TextNode(
            "![image](https://i.imgur.com/zjjcJKZ.png) this is a text and this is another one ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node, node2])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" this is a text and this is another one ", TextType.TEXT),
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
            ],
            new_nodes,
        )

