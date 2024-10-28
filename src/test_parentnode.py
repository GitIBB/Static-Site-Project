import unittest
from htmlnode import ParentNode, LeafNode

class TestParentNode(unittest.TestCase):
    
    def test_create_parent_node(self):
        node = ParentNode("div", [LeafNode("p", "Hello")])
        self.assertEqual(node.tag, "div")
        self.assertEqual(len(node.children), 1)

    def test_parent_node_without_tag(self):
        with self.assertRaises(ValueError):
            ParentNode(
                tag=None,
                children=[
                    LeafNode("b", "Bold text"),
                    LeafNode(None, "Normal text"),
                ]
            )

    def test_create_parent_node_multiple_children(self):
        node = ParentNode("div", [LeafNode("p", "Hello"), LeafNode("span", "World")])
        self.assertEqual(node.tag, "div")
        self.assertEqual(len(node.children), 2)

    def test_create_parent_node_no_children(self):
        with self.assertRaises(ValueError) as context:
            ParentNode("div", [])
        self.assertTrue("ParentNode must have children" in str(context.exception))

    def test_to_html_simple(self):
        node = ParentNode("div", [LeafNode("p", "Hello")])
        self.assertEqual(node.to_html(), "<div><p>Hello</p></div>")

    def test_to_html_nested(self):
        inner_node = ParentNode("div", [LeafNode("p", "Inner")])
        outer_node = ParentNode("section", [inner_node, LeafNode("span", "Outer")])
        self.assertEqual(outer_node.to_html(), "<section><div><p>Inner</p></div><span>Outer</span></section>")
