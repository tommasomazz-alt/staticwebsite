from enum import Enum
from inline_functions import text_to_textnodes
from textnode import text_node_to_html_node, TextNode, TextType
from htmlnode import HTMLNode, LeafNode, ParentNode

def markdown_to_blocks(markdown: str) -> list[str]:
    blocks = markdown.split("\n\n")
    result = []
    for block in blocks:
        block = block.strip()
        if block != "":
            result.append(block)

    return result

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def block_to_block_type(block: str) -> BlockType:
    lines = block.split("\n")

    if block.startswith(("#","##","###","####","#####","######")):
        return BlockType.HEADING

    if len(lines) >1 and block.startswith("```") and lines[-1].startswith("```"):
        return BlockType.CODE

    if block.startswith(">"):
        for line in lines:
            if not line.startswith(">"):
                return BlockType.PARAGRAPH
        return BlockType.QUOTE

    if block.startswith("- "):
        for line in lines:
            if not line.startswith("- "):
                return BlockType.PARAGRAPH
        return BlockType.UNORDERED_LIST

    if block.startswith("1. "):
        i = 1
        for line in lines:
            if not line.startswith(f"{i}. "):
                return BlockType.PARAGRAPH
            i += 1
        return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH

def text_to_children(text: str) -> list[LeafNode]:
    text_nodes = text_to_textnodes(text)
    result = []
    for node in text_nodes:
        result.append(text_node_to_html_node(node))
    return result

def paragraph_to_html_node(text: str) -> HTMLNode:
    lines = text.split("\n")
    cleaned = [line.strip() for line in lines]
    result = " ".join(cleaned)    
    leaf_nodes = text_to_children(result)
    parent_paragraph = ParentNode(
        "p",
        leaf_nodes,
        None
    )
    return parent_paragraph

def quote_to_html_node(text: str) -> HTMLNode:
    lines = text.split("\n")
    cleaned = [line[1:].strip() for line in lines]
    result = " ".join(cleaned)
    leaf_nodes = text_to_children(result)
    parent_quote = ParentNode(
        "blockquote",
        leaf_nodes,
        None
    )
    return parent_quote

def heading_to_html_node(text: str) -> HTMLNode:
    count = 0
    while text[count] == "#":
        count += 1
    cleaned = text[count+1:].strip()
    tag = f"h{count}"
    leaf_nodes = text_to_children(cleaned)
    parent_heading = ParentNode(
        tag,
        leaf_nodes,
        None
    )

    return parent_heading

def code_to_html_node(text: str) -> HTMLNode:
    cleaned = text[4:-3]
    code_text_node = TextNode(
        cleaned,
        TextType.CODE
    )
    code_html = text_node_to_html_node(code_text_node)

    parent = ParentNode(
        "pre",
        [code_html],
        None
    )

    return parent

def ulist_to_html_node(text: str) -> HTMLNode:
    lines = text.split("\n")
    cleaned = [line[1:].strip() for line in lines]
    u_lines = []
    for item in cleaned:
        leaf_nodes = text_to_children(item)
        u_line = ParentNode(
            "li",
            leaf_nodes,
            None
        )
        u_lines.append(u_line)

    parent = ParentNode(
        "ul",
        u_lines,
        None
    )

    return parent

def olist_to_html_node(text: str) -> HTMLNode:
    lines = text.split("\n")
    cleaned = []
    
    for i in range(0,len(lines)):
        prefix = len(f"{i + 1}")
        clean_line = lines[i][prefix + 2:]
        cleaned.append(clean_line)
    
    o_lines = []
    for item in cleaned:
        leaf_nodes = text_to_children(item)
        o_line = ParentNode(
            "li",
            leaf_nodes,
            None
        )
        o_lines.append(o_line)

    parent = ParentNode(
        "ol",
        o_lines,
        None
    )

    return parent

def markdown_to_html_node(markdown: str) -> HTMLNode:
    blocks = markdown_to_blocks(markdown)
    children = []

    for block in blocks:
        block_type = block_to_block_type(block)

        if block_type == BlockType.PARAGRAPH:
            children.append(paragraph_to_html_node(block))

        if block_type == BlockType.QUOTE:
            children.append(quote_to_html_node(block))

        if block_type == BlockType.HEADING:
            children.append(heading_to_html_node(block))

        if block_type == BlockType.CODE:
            children.append(code_to_html_node(block))

        if block_type == BlockType.UNORDERED_LIST:
            children.append(ulist_to_html_node(block))

        if block_type == BlockType.ORDERED_LIST:
            children.append(olist_to_html_node(block))
        
    parent = ParentNode(
        "div",
        children,
        None
    )

    return parent