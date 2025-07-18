import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode



class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        node1 = HTMLNode("div", "Hello, World!", [], {"class": "greeting"})
        # test props_to_html method
        self.assertEqual(node1.props_to_html(), 'class="greeting"')

    def test_leaf_to_html_p(self):
        node1 = LeafNode("p", "Hello, Worlds!")
        self.assertEqual(node1.to_html(), '<p>Hello, Worlds!</p>')
        node2 = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node2.to_html(), '<a href="https://www.google.com">Click me!</a>')

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )
    
    def test_to_html_with_props(self):
        child_node = LeafNode("span", "child", {"class": "child-class"})
        parent_node = ParentNode("div", [child_node], {"id": "parent-id"})
        self.assertEqual(
            parent_node.to_html(),
            '<div id="parent-id"><span class="child-class">child</span></div>',
        )

    def test_to_html_without_tag(self):
        with self.assertRaises(ValueError):
            ParentNode(None, []).to_html()

if __name__ == "__main__":
    unittest.main()