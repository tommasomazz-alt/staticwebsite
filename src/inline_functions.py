from textnode import TextNode, TextType

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