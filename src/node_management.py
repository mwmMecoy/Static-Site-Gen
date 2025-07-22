from textnode import TextNode, TextType, text_node_to_html_node
from htmlnode import LeafNode
import re

# example of split_nodes_delimited function
# It takes a list of "old nodes", a delimiter, and a text type. It should return a new list of nodes, where any "text" type nodes in the input list are (potentially) split into multiple nodes based on the syntax. For example, given the following input:
        # node = TextNode("This is text with a `code block` word", TextType.TEXT)
        # new_nodes = split_nodes_delimited([node], "`", TextType.CODE)
        # self.assertEqual(new_nodes[0], TextNode("This is text with a ", TextType.TEXT))
        # self.assertEqual(new_nodes[1], TextNode("code block", TextType.CODE))
        # self.assertEqual(new_nodes[2], TextNode(" word", TextType.TEXT))
    #The beauty of this function is that it will take care of inline code, bold, and italic text, all in one! The logic is identical, the delimiter and matching text_type are the only thing that changes, e.g. ** for bold, _ for italic, and a backtick for code. Also, because it operates on an input list, we can call it multiple times to handle different types of delimiters. The order in which you check for different delimiters matters, which actually simplifies implementation.
def split_nodes_delimited(old_nodes, delimiter, text_type):
    new_nodes = []
    
    for node in old_nodes:
        # Only process TEXT type nodes, others pass through unchanged
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
            
        # Split the text by the delimiter
        parts = node.text.split(delimiter)
        
        # If no delimiter found, add the original node
        if len(parts) == 1:
            new_nodes.append(node)
            continue
            
        # Check for unmatched delimiters (odd number of parts means unmatched)
        if len(parts) % 2 == 0:
            raise ValueError(f"Invalid markdown, unmatched delimiter: {delimiter}")
            
        # Process the parts alternately as TEXT and the specified text_type
        for i, part in enumerate(parts):
            if part:  # Skip empty parts
                if i % 2 == 0:  # Even indices are regular text
                    new_nodes.append(TextNode(part, TextType.TEXT))
                else:  # Odd indices are delimited text
                    new_nodes.append(TextNode(part, text_type))
    
    return new_nodes


def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type == TextType.TEXT:
            parts = re.split(r'!\[([^\]]+)\]\(([^)]+)\)', node.text)
            for i in range(0, len(parts), 3):
                new_nodes.append(TextNode(parts[i], TextType.TEXT))
                if i + 1 < len(parts):
                    new_nodes.append(TextNode(parts[i + 1], TextType.IMAGE, parts[i + 2]))
        else:
            new_nodes.append(node)
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type == TextType.TEXT:
            parts = re.split(r'\[([^\]]+)\]\(([^)]+)\)', node.text)
            for i in range(0, len(parts), 3):
                new_nodes.append(TextNode(parts[i], TextType.TEXT))
                if i + 1 < len(parts):
                    new_nodes.append(TextNode(parts[i + 1], TextType.LINK, parts[i + 2]))
        else:
            new_nodes.append(node)
    return new_nodes
    
def extract_markdown_images(text):
    image_pattern = r'!\[([^\]]+)\]\(([^)]+)\)'
    matches = re.findall(image_pattern, text)
    return [(alt_text, url) for alt_text, url in matches]

def extract_markdown_links(text):
    link_pattern = r'\[([^\]]+)\]\(([^)]+)\)'
    matches = re.findall(link_pattern, text)
    return [(anchor_text, url) for anchor_text, url in matches]

