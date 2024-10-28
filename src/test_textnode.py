import unittest

from textnode import TextNode, TextType, text_node_to_html_node
from htmlnode import LeafNode


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    
    def test_not_eq_different_text_type(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a textnode", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    
    def test_url_not_eq(self):
        node = TextNode("This is a test node", TextType.BOLD, url="https://first-url.com")
        node2 = TextNode("This is a test node", TextType.BOLD, url="https://second-url.com")
        self.assertNotEqual(node, node2)

    
    def test_different_text(self):
        node = TextNode("This is a test node", TextType.BOLD)
        node2 = TextNode("This is not test node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    
    def test_different_types(self):
        node = TextNode("This is a test node", TextType.BOLD)
        node2 = TextNode("this is a test node", TextType.TEXT)
        self.assertNotEqual(node, node2)
        

    def test_default_url(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD, url=None)
        self.assertEqual(node, node2)

    
    def test_case_sensitivity(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("this is a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    
    def test_full_attribute_equality(self):
        node = TextNode("This is a text node", TextType.BOLD, url="https://test-url.com")
        node2 = TextNode("This is a text node", TextType.BOLD, url="https://test-url.com")
        self.assertEqual(node, node2)
        


    def test_invalid_text_type(self):
        # Create a TextNode with a valid TextType, but we'll modify it to be invalid
        invalid_node = TextNode("text", TextType.TEXT)
        # Manually set the text_type to an invalid value
        invalid_node.text_type = "invalid_type"
        with self.assertRaises(Exception):
            text_node_to_html_node(invalid_node)

    def test_empty_text(self):
        empty_node = TextNode("", TextType.TEXT)
        result = text_node_to_html_node(empty_node)
        self.assertIsInstance(result, LeafNode)
        self.assertEqual(result.value, "")
        self.assertIsNone(result.tag)


    def test_very_long_text(self):
        long_text = "a" * 1000  # Create a string of 1000 'a' characters
        long_node = TextNode(long_text, TextType.BOLD)
        result = text_node_to_html_node(long_node)
        self.assertIsInstance(result, LeafNode)
        self.assertEqual(result.value, long_text)
        self.assertEqual(result.tag, "b")

    def test_special_characters(self):
        special_text = "Hello & <world>!"
        special_node = TextNode(special_text, TextType.ITALIC)
        result = text_node_to_html_node(special_node)
        self.assertIsInstance(result, LeafNode)
        self.assertEqual(result.value, special_text)
        self.assertEqual(result.tag, "i")



if __name__ == "__main__":
    unittest.main()