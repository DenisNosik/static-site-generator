from enum import Enum
from htmlnode import ParentNode, text_node_to_html_node
from inline_markdown import text_to_textnodes
from textnode import TextNode, TextType

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    result = []
    for block in blocks:
        if block == "":
            continue
        block = block.strip()
        result.append(block)
    return result

def block_to_block_type(markdown_block):
    lines = markdown_block.split("\n")
    if markdown_block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING
    if len(lines) > 1 and lines[0].startswith("```") and lines[-1].startswith("```"):
        return BlockType.CODE
    if markdown_block.startswith(">"):
        for line in lines:
            if not line.startswith(">"):
                return BlockType.PARAGRAPH
        return BlockType.QUOTE
    if markdown_block.startswith("- "):
        for line in lines:
            if not line.startswith("- "):
                return BlockType.PARAGRAPH
        return BlockType.UNORDERED_LIST
    if markdown_block.startswith("1. "):
        i = 1
        for line in lines:
            if not line.startswith(f"{i}. "):
                return BlockType.PARAGRAPH
            i += 1
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH
    
def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        block_type = block_to_block_type(block)
        match block_type:
            case BlockType.PARAGRAPH:
                formatted = block.replace("\n", " ")
                node = block_to_htmlnode("p", formatted)
                children.append(node)
            case BlockType.HEADING:
                heading_level, formatted = formatted_heading(block)
                node = block_to_htmlnode(heading_level, formatted)
                children.append(node)
            case BlockType.CODE:
                node = text_node_to_html_node(formatted_code(block))
                parent_code = ParentNode("pre", [node])
                children.append(parent_code)
            case BlockType.QUOTE:
                formatted = block.replace("> ", "")
                node = block_to_htmlnode("blockquote", formatted)
                children.append(node)
            case BlockType.UNORDERED_LIST:
                formatted = formatted_unordered_list(block)
                node = block_to_htmlnode("ul", formatted)
                children.append(node)
            case BlockType.ORDERED_LIST:
                formatted = formatted_ordered_list(block)
                node = block_to_htmlnode("ol", formatted)
                children.append(node)
    parent_node = ParentNode("div", children)
    return parent_node

def block_to_htmlnode(tag, text):
    children = text_to_children(text)
    node = ParentNode(tag, children)
    return node

def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    html_nodes = []
    for text_node in text_nodes:
        html_nodes.append(text_node_to_html_node(text_node))
    return html_nodes 

def formatted_heading(block):
    heading_level = 0
    for char in block:
        if char == "#":
            heading_level += 1
        else:
            break
    formatted = block[heading_level + 1 :]
    return (f"h{heading_level}", formatted)

def formatted_code(block):
    formatted = block.replace("```", "").lstrip("\n")
    text_node = TextNode(formatted, TextType.CODE)
    return text_node

def formatted_unordered_list(block):
    lines = block.split("\n")
    formatted = ""
    for line in lines:
        formatted_line = line.replace("- ", "")
        formatted_line = f"<li>{formatted_line}</li>"
        formatted += formatted_line
    return formatted
        
def formatted_ordered_list(block):
    lines = block.split("\n")
    formatted = ""
    i = 1
    for line in lines:
        formatted_line = line.replace(f"{i}. ", "")
        formatted_line = f"<li>{formatted_line}</li>"
        formatted += formatted_line
        i += 1
    return formatted
    
        
