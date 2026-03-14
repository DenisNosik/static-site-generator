import re
from textnode import TextNode, TextType


def text_to_textnodes(text):
    new_nodes = [TextNode(text, TextType.TEXT),]
    new_nodes = split_nodes_delimiter(new_nodes, "**", TextType.BOLD)
    new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
    new_nodes = split_nodes_delimiter(new_nodes, "`", TextType.CODE)
    new_nodes = split_nodes_image(new_nodes)
    new_nodes = split_nodes_link(new_nodes)
    return new_nodes

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        
        splitted_nodes = []
        sections = old_node.text.split(delimiter)
        
        if len(sections) % 2 == 0:
            raise ValueError(f"ERROR: Invalid Markdown {delimiter}")
        
        for i in range(len(sections)):
            if sections[i] == "":
                continue
            if i % 2 == 0:
                splitted_nodes.append(TextNode(sections[i], TextType.TEXT))
            else:
                splitted_nodes.append(TextNode(sections[i], text_type))
        
        new_nodes.extend(splitted_nodes)

    return new_nodes

def split_nodes_image(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue

        sections = []
        extracted_images = extract_markdown_images(old_node.text)
        if len(extracted_images) == 0:
            new_nodes.append(old_node)
            continue
        
        original_text = old_node.text
        
        for image_alt, image_link in extracted_images:
            sections = original_text.split(f"![{image_alt}]({image_link})", 1)
            if len(sections) != 2:
                raise ValueError("invalid markdown, image section not closed")
            if sections[0] == "":
                new_nodes.append(TextNode(image_alt, TextType.IMAGE, image_link))
                original_text = sections[1]
                continue
            new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(image_alt, TextType.IMAGE, image_link))
            original_text = sections[1]
        
        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.TEXT))

    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue

        sections = []
        extracted_links = extract_markdown_links(old_node.text)
        if len(extracted_links) == 0:
            new_nodes.append(old_node)
            continue
        
        original_text = old_node.text
        
        for link_anchor, link in extracted_links:
            sections = original_text.split(f"[{link_anchor}]({link})", 1)
            if sections[0] == "":
                new_nodes.append(TextNode(link_anchor, TextType.LINK, link))
                original_text = sections[1]
                continue
            new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(link_anchor, TextType.LINK, link))
            original_text = sections[1]
        
        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.TEXT))

    return new_nodes

def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
