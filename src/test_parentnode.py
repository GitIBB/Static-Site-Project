import unittest
from htmlnode import ParentNode, LeafNode

class TestParentNode(unittest.TestCase):
    
    def test_create_parent_node(self):
        node = ParentNode("div", [LeafNode("p", "Hello")])
        self.assertEqual(node.tag, "div")
        self.assertEqual(len(node.children), 1)

    
    def test_create_parent_node_without_tag(self):
        # Test creating a ParentNode without a tag
        with self.assertRaises(ValueError):
            ParentNode(None, [LeafNode("p", "Hello")])


    def test_with_no_children(self):
        # Test creating a ParentNode without children
        with self.assertRaises(ValueError):
            ParentNode("div", [])

    
    def test_to_html(self):
        # Create a ParentNode with LeafNode children
        node = ParentNode("div", [
            LeafNode("p", "Hello"),
            LeafNode("span", "World")
        ])
        expected_html = "<div><p>Hello</p><span>World</span></div>"
        
        #Check if the output of to_html matches the expected HTML
        self.assertEqual(node.to_html(), expected_html)

    
    def test_to_html_nested(self):
        # Create nested Parentnodes and LeafNodes
        child_node = ParentNode("p", [
            LeafNode("b", "Bold text"),
            LeafNode("span", "Normal text") 
        ])
        parent_node = ParentNode("div", [child_node])
        expected_html = "<div><p><b>Bold text</b>Normal text</p></div>"

        # Check if the output of to_html matches the expected HTML
        self.assertEqual(parent_node.to_html(), expected_html)

    def test_to_html_multiple_children(self):
    # Create a ParentNode with multiple LeafNode children
        node = ParentNode("ul", [
            LeafNode("li", "Item 1"),
            LeafNode("li", "Item 2"),
            LeafNode("li", "Item 3")
    ])
        expected_html = "<ul><li>Item 1</li><li>Item 2</li><li>Item 3</li></ul>"
    
    # Check if the output of to_html matches the expected HTML
        self.assertEqual(node.to_html(), expected_html)


    def test_create_parent_node_with_empty_tag(self):
    # Test creating a ParentNode with an empty string as a tag
        with self.assertRaises(ValueError):
            ParentNode("", [LeafNode("p", "Empty tag test")])



