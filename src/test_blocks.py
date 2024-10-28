import unittest
from block_functions import markdown_to_blocks, block_to_block_type, markdown_to_html_node

class TestBlocks(unittest.TestCase):

    def test_markdown_to_blocks(self):

        test_markdown = """# This is a heading

    This is a paragraph of text. It has some **bold** and *italic* words inside of it.

    * This is the first list item in a list block
    * This is a list item
    * This is another list item"""

        result = markdown_to_blocks(test_markdown)
        
        #Assert
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0], "# This is a heading")
        self.assertEqual(result[1], "This is a paragraph of text. It has some **bold** and *italic* words inside of it.")
        self.assertEqual(result[2], "* This is the first list item in a list block\n* This is a list item\n* This is another list item")

    def test_single_block(self):
        block = "Hello World"
        result = markdown_to_blocks(block)
        self.assertEqual(result[0], "Hello World")

    
    def multi_lines_single_newline(self):
        blocks = """# This is a heading
        This is a paragraph of text. It has some **bold** and *italic* words inside of it.
        * This is the first list item in a list block
        * This is a list item
        * This is another list item"""
        result = markdown_to_blocks(block)
        self.assertEqual(
            result[0], """# This is a heading
        This is a paragraph of text. It has some **bold** and *italic* words inside of it.
        * This is the first list item in a list block
        * This is a list item
        * This is another list item"""
                         )
        
    def test_markdown_seperation(self):
        # Multiple blocks with proper separation
        text = "Block 1\n\nBlock 2\n\nBlock 3"
        expected = ["Block 1", "Block 2", "Block 3"]
        self.assertEqual(markdown_to_blocks(text), expected)



    def test_markdown_consecutive_empty_lines(self):
        # Multiple consecutive empty lines
        text = "First block\n\n\n\n\nLast block"
        expected = ["First block", "Last block"]
        self.assertEqual(markdown_to_blocks(text), expected)

    def test_empty_blocks(self):
        # Text with empty blocks between content
        text = "First block\n\n\n\n   \n\nSecond block\n\n  \n  \nThird block"
        expected = ["First block", "Second block", "Third block"]
        self.assertEqual(markdown_to_blocks(text), expected)


    def test_empty_start_end(self):
        # Text with empty blocks at start and end
        text = "\n\n  \nFirst block\n\nSecond block\n\n  \n"
        expected = ["First block", "Second block"]
        self.assertEqual(markdown_to_blocks(text), expected)


    # block_to_block_type tests

    def test_headings(self):
         # Test heading variations
        self.assertEqual(block_to_block_type("# Heading"),"heading")
        self.assertEqual(block_to_block_type("###### Heading"), "heading")
    
    def test_invalid_headings(self):
    # Test invalid headings
        self.assertEqual(block_to_block_type("####### Heading"), "paragraph")
        self.assertEqual(block_to_block_type("#Heading"), "paragraph")  # no space after #
    
    def test_code_blocks(self):
        self.assertEqual(block_to_block_type("```\nsome code\n```"), "code")

    def test_quote_blocks(self):
        self.assertEqual(block_to_block_type(">some quote\n>somequote"), "quote")
    
    def test_ordered_lists(self):
        self.assertEqual(block_to_block_type("1. list line one\n2. list line two\n3. list line three"), "ordered_list")

    def test_unordered_lists(self):
        self.assertEqual(block_to_block_type("* some text\n-some words\n*some text again"), "unordered_list")

    def test_paragraphs(self):
        self.assertEqual(block_to_block_type("?? very str4nge - .. fo rmat ++++ ing ```\n1. indeed !!! messy"""), "paragraph")
    

    # Test markdownToHTML

    def test_single_heading(self):
        markdown = "# Heading 1"
        node = markdown_to_html_node(markdown)
        self.assertEqual(node.to_html(), "<div><h1>Heading 1</h1></div>")
    
    def test_paragraphs(self):
        markdown = "First paragraph.\n\nSecond paragraph."
        node = markdown_to_html_node(markdown)
        self.assertEqual(node.to_html(), "<div><p>First paragraph.</p><p>Second paragraph.</p></div>")

    def test_multiple_headings(self):
        markdown = "# Heading 1\n\n## Heading 2\n\n### Heading 3"
        node = markdown_to_html_node(markdown)
        self.assertEqual(node.to_html(), "<div><h1>Heading 1</h1><h2>Heading 2</h2><h3>Heading 3</h3></div>")

    def test_unordered_list(self):
        markdown = "- Item 1\n- Item 2"
        node = markdown_to_html_node(markdown)
        self.assertEqual(node.to_html(), "<div><ul><li>Item 1</li><li>Item 2</li></ul></div>")

    def test_block_quote(self):
        markdown = "> Quote one\n> Quote two"
        node = markdown_to_html_node(markdown)
        self.assertEqual(node.to_html(), "<div><blockquote><p>Quote one</p><p>Quote two</p></blockquote></div>")

    def test_code_block(self):
        markdown = "```\ncode\n```\n\n```\ncode\n```"
        node = markdown_to_html_node(markdown)
        self.assertEqual(node.to_html(), "<div><pre><code>code</code></pre><pre><code>code</code></pre></div>")

    def test_mixed_content(self):
        markdown = "# Heading\n\nThis is a paragraph with **bold** text and *italic* text.\n\n```\ncode\n```"
        node = markdown_to_html_node(markdown)
        expected_html = (
            "<div>"
            "<h1>Heading</h1>"
            "<p>This is a paragraph with <strong>bold</strong> text and <em>italic</em> text.</p>"
            "<pre><code>code</code></pre>"
            "</div>"
        )
        self.assertEqual(node.to_html(), expected_html)


if __name__ == '__main__':
    unittest.main()
