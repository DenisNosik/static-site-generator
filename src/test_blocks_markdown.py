import unittest
from blocks_markdown import (
    BlockType, markdown_to_blocks, block_to_block_type,
    markdown_to_html_node
)
from main import extract_title


class TestMarkdownToBlocks(unittest.TestCase):
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
    
    def test_markdown_to_blocks_second(self):
        md = """
# This is a heading

This is a paragraph of text. It has some **bold** and _italic_ words inside of it.

- This is the first list item in a list block
- This is a list item
- This is another list item
- This is last list item
        """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "# This is a heading",
                "This is a paragraph of text. It has some **bold** and _italic_ words inside of it.",
                "- This is the first list item in a list block\n- This is a list item\n- This is another list item\n- This is last list item",
            ],
        )

class TestBlockToBlockType(unittest.TestCase):
    def test_paragraph(self):
        md = "123This is just a paragraph of text.123"
        blocks = markdown_to_blocks(md)
        block_type = block_to_block_type(blocks[0])
        self.assertEqual(
            BlockType.PARAGRAPH,
            block_type
        )
    
    def test_heading(self):
        md = "# This is a heading"
        blocks = markdown_to_blocks(md)
        block_type = block_to_block_type(blocks[0])
        self.assertEqual(
            BlockType.HEADING,
            block_type
        )
    
    def test_code(self):
        md = """
```
this md is a code md
```
        """
        blocks = markdown_to_blocks(md)
        block_type = block_to_block_type(blocks[0])
        self.assertEqual(
            BlockType.CODE,
            block_type
        )
    
    def test_ordered_list(self):
        md = """
1. this is an ordered_list
2. very cool tho
3. hello world
        """
        blocks = markdown_to_blocks(md)
        block_type = block_to_block_type(blocks[0])
        self.assertEqual(
            BlockType.ORDERED_LIST,
            block_type
        )
    
    def test_larghe_md(self):
        md = """
# This is a heading

This is a paragraph of text. It has some **bold** and _italic_ words inside of it.

- This is the first list item in a list block
- This is a list item
- This is another list item
- This is last list item
        """
        blocks = markdown_to_blocks(md)
        block_type = block_to_block_type(blocks[2])
        self.assertEqual(
            BlockType.UNORDERED_LIST,
            block_type
        )

class TestBlockToHTML(unittest.TestCase):
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
    
    def test_heading_and_unorderd_list(self):
        md = """
# This is a heading

This is a paragraph of text. It has some **bold** and _italic_ words inside of it.

- This is the first list item in a list block
- This is a list item
- This is another list item
        """
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>This is a heading</h1><p>This is a paragraph of text. It has some <b>bold</b> and <i>italic</i> words inside of it.</p><ul><li>This is the first list item in a list block</li><li>This is a list item</li><li>This is another list item</li></ul></div>",
        )
    
    def test_heading_and_orderd_list(self):
        md = """
# This is a heading

This is a paragraph of text. It has some **bold** and _italic_ words inside of it.

1. This is the first list item in a list block
2. This is a list item
3. This is another list item
        """
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>This is a heading</h1><p>This is a paragraph of text. It has some <b>bold</b> and <i>italic</i> words inside of it.</p><ol><li>This is the first list item in a list block</li><li>This is a list item</li><li>This is another list item</li></ol></div>",
        )
    
    def test_headings(self):
        md = """
###### This is a heading 6
        """
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h6>This is a heading 6</h6></div>",
        )
    