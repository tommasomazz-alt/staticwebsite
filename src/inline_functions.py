from textnode import TextNode, TextType
import re

def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
    split_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            split_nodes.append(node)
        
        #Logic for text type split and node creation:
        #- use the split() function with the related delimiter, for each type
        #- if len == 1 then there is no delimiter of the text types we're checking (bold, italics, code) so we skip this
        #- if the len of the split text is even, there's some missing delimiter 
        #- if split text is "" no need to create a node with it
        #- even indexes of the good split list are text types. 
        #- odd indexes of the good split list are delimited text types.
        
        else:
            
            node_words = node.text.split(delimiter)

            if len(node_words) == 1:
                split_nodes.append(node)
                continue

            elif len(node_words) % 2 == 0:
                raise Exception("Invalid Markdown syntax: missing opening or closing delimiter")
            
            for i in range(len(node_words)):
                if node_words[i] == "":
                    continue
                elif i % 2 == 0:
                    new_node = TextNode(node_words[i], TextType.TEXT)
                    split_nodes.append(new_node)
                elif i % 2 != 0:
                    new_node = TextNode(node_words[i], text_type)
                    split_nodes.append(new_node)
    
    return split_nodes

def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    split_nodes = []
    for node in old_nodes:
        remaining_text = node.text
        if node.text_type != TextType.TEXT:
            split_nodes.append(node)
            continue
        
        images = extract_markdown_images(node.text)
        if len(images) == 0:
            split_nodes.append(node)
            continue

        for group in images:
            node_words = remaining_text.split(f"![{group[0]}]({group[1]})", 1)

            if len(node_words) != 2:
                raise ValueError("Invalid markdown, image section not closed")

            if node_words[0] != "":
                new_node = TextNode(node_words[0], TextType.TEXT)
                split_nodes.append(new_node)

            new_node = TextNode(group[0], TextType.IMAGE, group[1])
            split_nodes.append(new_node)

            remaining_text = node_words[1]

        if remaining_text != "":
            new_node = TextNode(remaining_text, TextType.TEXT)
            split_nodes.append(new_node)

    return split_nodes

def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    split_nodes = []
    for node in old_nodes:
        remaining_text = node.text
        if node.text_type != TextType.TEXT:
            split_nodes.append(node)
            continue
        
        links = extract_markdown_links(node.text)
        if len(links) == 0:
            split_nodes.append(node)
            continue

        for group in links:
            node_words = remaining_text.split(f"[{group[0]}]({group[1]})", 1)

            if len(node_words) != 2:
                raise ValueError("Invalid markdown, links section not closed")

            if node_words[0] != "":
                new_node = TextNode(node_words[0], TextType.TEXT)
                split_nodes.append(new_node)

            new_node = TextNode(group[0], TextType.LINK, group[1])
            split_nodes.append(new_node)

            remaining_text = node_words[1]

        if remaining_text != "":
            new_node = TextNode(remaining_text, TextType.TEXT)
            split_nodes.append(new_node)

    return split_nodes

def extract_markdown_images(text: str) -> list[tuple[str, str]]:
    pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    regex_images = re.findall(pattern, text)
    return regex_images


def extract_markdown_links(text: str) -> list[tuple[str, str]]:
    pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    regex_links = re.findall(pattern, text)
    return regex_links

def text_to_textnodes(text: str) -> list[TextNode]:
    Starting_node = TextNode(text, TextType.TEXT)
    Starting_nodes = [Starting_node]

    split_bold = split_nodes_delimiter(Starting_nodes,"**",TextType.BOLD)
    split_italics = split_nodes_delimiter(split_bold,"_",TextType.ITALIC)
    split_code = split_nodes_delimiter(split_italics,"`",TextType.CODE)
    split_images = split_nodes_image(split_code)
    split_links = split_nodes_link(split_images)

    return split_links
