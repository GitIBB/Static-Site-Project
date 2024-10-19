import unittest

from htmlnode import HtmlNode
from htmlnode import LeafNode

#BEST TO GO THROUGH THIS CODE LATER AND UNDERSTAND IT BETTER!
class TestLeafNode(unittest.TestCase):

    def test_leaf_node_with_value(self):
    # Test that a LeafNode is properly created when a 'value' is provided.
        try:
            node = LeafNode(value="This is a paragraph", tag="p")
            # If no exception occurs, the test should pass
            self.assertIsNotNone(node)  # Optional: Assert that node is indeed created
        except ValueError:
            self.fail("LeafNode raised a ValueError unexpectedly!")

    def test_to_html_raises_error_when_value_is_empty(self):
        # Test to_html() raises ValueError if instantiated with an empty value
        leaf_node = LeafNode(tag="p", value="")
        with self.assertRaises(ValueError):
            leaf_node.to_html()

    def test_plain_text_no_tag(self):
        # Test the rendering when there is no tag
        leaf_node = LeafNode(value="Plain text")
        self.assertEqual(leaf_node.to_html(), "Plain text")

    def test_single_tag_without_attributes(self):
        # Test a tag without any attributes
        leaf_node = LeafNode(value="Hello, World!", tag="p")
        self.assertEqual(leaf_node.to_html(), "<p>Hello, World!</p>")

    def test_single_tag_with_attributes(self):
        # Test the rendering of a tag with attributes
        leaf_node = LeafNode(value="Link", tag="a", props={"href": "https://example.com"})
        self.assertEqual(leaf_node.to_html(), '<a href="https://example.com">Link</a>')

if __name__ == '__main__':
    unittest.main()