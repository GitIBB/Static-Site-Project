import re
import unittest
from extract_markdown import extract_markdown_images, extract_markdown_links

class TestExtraction(unittest.TestCase):

    def test_simple_markdown_image(self):
        text = "Here is an ![alt text](https://example.com/image1.png) and another ![image](https://example.com/image2.png)."
        expected_output = [
            ("alt text", "https://example.com/image1.png"),
            ("image", "https://example.com/image2.png")
        ]
        self.assertEqual(extract_markdown_images(text), expected_output)


    def test_simple_markdown_link(self):
        text = "Text with a link [to google](https://google.com) and [to youtube](https://youtube.com)"
        expected_output = [
            ("to google", "https://google.com"),
            ("to youtube", "https://youtube.com")
        ]
        self.assertEqual(extract_markdown_links(text), expected_output)

    
    def test_no_images_generic_text(self):
        text = "This is just ordinary text without any markdown images."
        expected_output = []
        self.assertEqual(extract_markdown_images(text), expected_output)

    def test_no_images_with_links(self):
        text = "Here is a link to [Boot.dev](https://www.boot.dev) but no images."
        expected_output = []
        self.assertEqual(extract_markdown_images(text), expected_output)

    def test_irregular_spacing(self):
        text = "Here is an image with space ![ alt text ] ( https://example.com/image.png ) "
        expected_output = [(" alt text ", " https://example.com/image.png ")]
        self.assertNotEqual(extract_markdown_images(text), expected_output)

    def test_empty_alt_text(self):
        text = "![](https://example.com/no-alt-text.png)"
        expected_output = [("", "https://example.com/no-alt-text.png")]
        self.assertEqual(extract_markdown_images(text), expected_output)

    def test_unusual_urls(self):
        text = "![alt](https://example.com/image.png?width=500&name=example)"
        expected_output = [("alt", "https://example.com/image.png?width=500&name=example")]
        self.assertEqual(extract_markdown_images(text), expected_output)

    def test_urls_with_query_parameters(self):
        text = "![alt text](https://example.com/image.png?size=large&color=blue)"
        expected_output = [("alt text", "https://example.com/image.png?size=large&color=blue")]
        self.assertEqual(extract_markdown_images(text), expected_output)

    def test_urls_with_fragments(self):
        text = "![another image](https://example.com/image.png#section2)"
        expected_output = [("another image", "https://example.com/image.png#section2")]
        self.assertEqual(extract_markdown_images(text), expected_output)

    def test_nested_links_and_images(self):
        text = "Here's an image ![hero](https://example.com/hero.png) and a [homepage link](https://example.com)"
        expected_images = [("hero", "https://example.com/hero.png")]
        self.assertEqual(extract_markdown_images(text), expected_images)
    
        expected_links = [("homepage link", "https://example.com")]
        self.assertEqual(extract_markdown_links(text), expected_links)

    def test_missing_closing_parenthesis(self):
        text = "Here's a link with a missing parenthesis [example link](https://example.com"
        expected_output = []  # since the markdown is incomplete, we expect no results
        self.assertEqual(extract_markdown_links(text), expected_output)

    def test_misplaced_brackets(self):
        text = "Here's a link with misplaced brackets [example link(https://example.com)]"
        expected_output = []  # the incorrect bracket placement means no correct markdown is present
        self.assertEqual(extract_markdown_links(text ), expected_output)

if __name__ == "__main__":
    unittest.main()