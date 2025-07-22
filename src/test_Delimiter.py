import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode
from textnode import TextNode, TextType, text_node_to_html_node
from node_management import split_nodes_delimited, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link

class TestNodeManagement(unittest.TestCase):
    def test_split_nodes_delimited(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimited([node], "`", TextType.CODE)
        self.assertEqual(new_nodes[0], TextNode("This is text with a ", TextType.TEXT))
        self.assertEqual(new_nodes[1], TextNode("code block", TextType.CODE))
        self.assertEqual(new_nodes[2], TextNode(" word", TextType.TEXT))

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a [link](https://example.com)"
        )
        self.assertListEqual([("link", "https://example.com")], matches)

    #test split_nodes_image and split_nodes_link
    def test_split_nodes_image(self):
        node = TextNode("This is an ![image](https://i.imgur.com/zjjcJKZ.png)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertEqual(new_nodes[0], TextNode("This is an ", TextType.TEXT))
        self.assertEqual(new_nodes[1], TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"))
    
    def test_split_nodes_link(self):
        node = TextNode("This is a [link](https://example.com)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertEqual(new_nodes[0], TextNode("This is a ", TextType.TEXT))
        self.assertEqual(new_nodes[1], TextNode("link", TextType.LINK, "https://example.com"))
    
if __name__ == "__main__":
    unittest.main()