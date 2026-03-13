from textnode import TextNode, TextType


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    if len(old_nodes) == 0:
        raise ValueError("ERROR: old_nodes list is empty")
    
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        
        splited_nodes = []
        selection = old_node.text.split(delimiter)
        
        if len(selection) % 2 == 0:
            raise ValueError(f"ERROR: Invalid Markdown {delimiter}")
        
        for i in range(len(selection)):
            if selection[i] == "":
                continue
            if i % 2 == 0:
                splited_nodes.append(TextNode(selection[i], TextType.TEXT))
            else:
                splited_nodes.append(TextNode(selection[i], text_type))
        
        new_nodes.extend(splited_nodes)

    return new_nodes
