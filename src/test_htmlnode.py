import unittest

from htmlnode import HtmlNode

class TestHtmlNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HtmlNode(props={"href": "https://example.com"})
        expected_output = ' href="https://example.com"'
        self.assertEqual(node.props_to_html(), expected_output)

    def test_default_values(self):
        node = HtmlNode()
        self.assertIsNone(node.tag)
        self.assertIsNone(node.value)
        self.assertIsInstance(node.children, type(None))
        self.assertEqual(node.props, {})

    def test_repr(self):
        node = HtmlNode(tag="div", value="Test", children=[], props={"class": "test-div"})
        expected_repr ="HtmlNode(tag=div, value=Test, children=[], props={'class': 'test-div'})"
        self.assertEqual(repr(node), expected_repr)

if __name__ == '__main__':
    unittest.main()