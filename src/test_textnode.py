import unittest

from textnode import TextNode, TextType


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
        node2 = TextNode("this is a test node", TextType.NORMAL)
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

    

    


if __name__ == "__main__":
    unittest.main()