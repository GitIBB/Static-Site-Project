import unittest

from textnode import TextNode, TextType
from split_functions import split_nodes_delimiter, split_nodes_image, split_nodes_link, text_to_textnodes

class TestDelimiter(unittest.TestCase):
    def test_code_delimiter(self):
        node = TextNode("This is `code` in the text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)

        # Check the number of nodes
        assert len(new_nodes) == 3, f"Unexpected number of nodes. Got: {len(new_nodes)}"

        # Check each node's content and type
        expected_contents = ["This is ", "code", " in the text"]
        expected_types = [TextType.TEXT, TextType.CODE, TextType.TEXT]

        for index, node in enumerate(new_nodes):
            assert node.text == expected_contents[index], f"Unexpected content: Got: {node.text}"
            assert node.text_type == expected_types[index], f"Unexpected type. Got: {node.text_type}"


    def test_bold_delimiter(self):
        node = TextNode("This is **bold** text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
    
        # Check the number of nodes
        assert len(new_nodes) == 3, f"Unexpected number of nodes. Got: {len(new_nodes)}"

        # Check each node's content and type
        expected_contents = ["This is ", "bold", " text"]
        expected_types = [TextType.TEXT, TextType.BOLD, TextType.TEXT]
    
        for idx, node in enumerate(new_nodes):
            assert node.text == expected_contents[idx], f"Unexpected content. Got: {node.text}"
            assert node.text_type == expected_types[idx], f"Unexpected type. Got: {node.text_type}"


    def test_italic_delimiter(self):
        node = TextNode("This is *italic* text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "*", TextType.ITALIC)
    
        # Check the number of nodes
        assert len(new_nodes) == 3, f"Unexpected number of nodes. Got: {len(new_nodes)}"

        # Check each node's content and type
        expected_contents = ["This is ", "italic", " text"]
        expected_types = [TextType.TEXT, TextType.ITALIC, TextType.TEXT]
    
        for index, node in enumerate(new_nodes):
            assert node.text == expected_contents[index], f"Unexpected content. Got: {node.text}"
            assert node.text_type == expected_types[index], f"Unexpected type. Got: {node.text_type}"


    def test_empty_delimiter(self):
        node = TextNode("This is ** ** text", TextType.TEXT)
        with self.assertRaises(ValueError) as context:
            split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(str(context.exception), "Empty content between delimiters")


    def test_unclosed_delimiter(self):
        node = TextNode("This is *incomplete", TextType.TEXT)
        with self.assertRaises(ValueError) as context:
            split_nodes_delimiter([node], "*", TextType.ITALIC)
        self.assertEqual(str(context.exception), "Invalid Markdown")
    # Three parameters, old_nodes, delimiter and text_type
    # Three variables,index, part, new_nodes


    def test_multiple_delimiters(self):
        node = TextNode("Text with `code` and `more code` here", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
    
        self.assertEqual(len(new_nodes), 5)
        self.assertEqual(new_nodes[0].text, "Text with ")
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[1].text, "code")
        self.assertEqual(new_nodes[1].text_type, TextType.CODE)
        self.assertEqual(new_nodes[2].text, " and ")
        self.assertEqual(new_nodes[2].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[3].text, "more code")
        self.assertEqual(new_nodes[3].text_type, TextType.CODE)
        self.assertEqual(new_nodes[4].text, " here")
        self.assertEqual(new_nodes[4].text_type, TextType.TEXT)   

    def test_non_text_node(self):
        # Create a non-text node (like a bold node)
        bold_node = TextNode("This is bold text", TextType.BOLD)
        # Try to split it with a code delimiter
        result = split_nodes_delimiter([bold_node], "`", TextType.CODE)
    
        # Verify that the node wasn't changed
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].text, "This is bold text")
        self.assertEqual(result[0].text_type, TextType.BOLD)


if __name__ == '__main__':
    unittest.main()


class TestSplits(unittest.TestCase):
    
    def test_split_image(self):
        node = TextNode("Text before image ![alt text](image url) text after image", TextType.TEXT)
        new_nodes = split_nodes_image([node])

        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[0].text, "Text before image ")

        self.assertEqual(new_nodes[1].text_type, TextType.IMAGE)
        self.assertEqual(new_nodes[1].text, "alt text")
        self.assertEqual(new_nodes[1].url, "image url")

        self.assertEqual(new_nodes[2].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[2].text, " text after image")
    

    def test_split_link(self):
        node = TextNode("Text before link [anchor text](link url) text after link", TextType.TEXT)
        new_nodes = split_nodes_link([node])

        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[0].text, "Text before link ")

        self.assertEqual(new_nodes[1].text_type, TextType.LINK)
        self.assertEqual(new_nodes[1].text, "anchor text")
        self.assertEqual(new_nodes[1].url, "link url")

        self.assertEqual(new_nodes[2].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[2].text, " text after link")



    def test_split_link_no_links(self):
        node = TextNode("This is plain text without any links.", TextType.TEXT)
        new_nodes = split_nodes_link([node])

        # The result should be a single node identical to input
        self.assertEqual(len(new_nodes), 1)
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[0].text, "This is plain text without any links.")

    def test_split_image_no_images(self):
        node = TextNode("This is plain text without any images.", TextType.TEXT)
        new_nodes = split_nodes_image([node])

        # The result should be a single node identical to input
        self.assertEqual(len(new_nodes), 1)
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[0].text, "This is plain text without any images.")



    def test_split_link_multiple_links(self):
        node = TextNode(
            "First part of text [first link](first-url) middle text [second link](second-url) last part",
            TextType.TEXT
            )
        new_nodes = split_nodes_link([node])

        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[0].text, "First part of text ")
        self.assertEqual(new_nodes[1].text_type, TextType.LINK)
        self.assertEqual(new_nodes[1].text, "first link")
        self.assertEqual(new_nodes[1].url, "first-url")
        self.assertEqual(new_nodes[2].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[2].text, " middle text ")
        self.assertEqual(new_nodes[3].text_type, TextType.LINK)
        self.assertEqual(new_nodes[3].text, "second link")
        self.assertEqual(new_nodes[3].url, "second-url")
        self.assertEqual(new_nodes[4].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[4].text, " last part")

    def test_split_image_multiple_images(self):
        node = TextNode(
            "Welcome to the gallery ![first image](first-url) and ![second image](second-url) enjoy!",
            TextType.TEXT
            )
        new_nodes = split_nodes_image([node])

        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[0].text, "Welcome to the gallery ")
        self.assertEqual(new_nodes[1].text_type, TextType.IMAGE)
        self.assertEqual(new_nodes[1].text, "first image")
        self.assertEqual(new_nodes[1].url, "first-url")
        self.assertEqual(new_nodes[2].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[2].text, " and ")
        self.assertEqual(new_nodes[3].text_type, TextType.IMAGE)
        self.assertEqual(new_nodes[3].text, "second image")
        self.assertEqual(new_nodes[3].url, "second-url")
        self.assertEqual(new_nodes[4].text_type, TextType.TEXT)


    def test_split_adjacent_links_and_images(self):
        input_text = "![image1](url1)[link1](url2)"
        node = TextNode(input_text, TextType.TEXT)

        # You can either do this in two steps or ensure one function handles both
        intermediate_nodes = split_nodes_image([node])  # First split images
        final_nodes = split_nodes_link(intermediate_nodes)  # Then split links
    
        # Now, we can assert that we have the correct number and type of nodes
        assert len(final_nodes) == 2
    
        # Check that the first node is an image node
        assert final_nodes[0].text == "image1"
        assert final_nodes[0].text_type == TextType.IMAGE
        assert final_nodes[0].url == "url1"

        # Check that the second node is a link node
        assert final_nodes[1].text == "link1"
        assert final_nodes[1].text_type == TextType.LINK
        assert final_nodes[1].url == "url2"


    def test_no_empty_text_nodes(self):
        input_text = "![](url1) some text []()"
        node = TextNode(input_text, TextType.TEXT)
        
        intermediate_nodes = split_nodes_image([node])
        final_nodes = split_nodes_link(intermediate_nodes)

        # Verify no nodes have empty text after splitting
        for n in final_nodes:
            self.assertNotEqual(node.text, "", f"Empty node found: {n}")


    def test_text_to_textnodes(self):
        input_text = "A **bold** statement with *italic* flair and a `code snippet`. ![pic](image.png)"
    
        expected_nodes = [
            TextNode("A ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" statement with ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" flair and a ", TextType.TEXT),
            TextNode("code snippet", TextType.CODE),
            TextNode(". ", TextType.TEXT),
            TextNode("pic", TextType.IMAGE, "image.png")
        ]
    
        actual_nodes = text_to_textnodes(input_text)
        self.assertEqual(actual_nodes, expected_nodes)

    def test_empty_input(self):
        input_text = ""
    
        expected_nodes = []

        actual_nodes = text_to_textnodes(input_text)
        self.assertEqual(actual_nodes, expected_nodes)

    def test_plain_text(self):
        input_text = "just some plain text"

        expected_nodes = [
            TextNode("just some plain text", TextType.TEXT)
        ]
        
        actual_nodes = text_to_textnodes(input_text)
        self.assertEqual(actual_nodes, expected_nodes)

    def test_unclosed_bold(self):
        input_text = "Unfinished **bold"
        # Expecting the function to raise a ValueError for an invalid markdown
        try:
            text_to_textnodes(input_text)
        except ValueError as e:
            assert str(e) == "Invalid Markdown"

    def test_empty_bold(self):
        input_text = "This is a ** ** test"
        # Expecting ValueError for empty content between delimiters
        try:
            text_to_textnodes(input_text)
        except ValueError as e:
            assert str(e) == "Empty content between delimiters"



    def test_markdown_text_parsing(self):
        text = "Start **bold** middle *italic* and `code` and a [Boot.dev link](https://boot.dev)"
        expected_output = [
            TextNode("Start ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" middle ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" and ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" and a ", TextType.TEXT),
            TextNode("Boot.dev link", TextType.LINK, "https://boot.dev")
        ]
        result = text_to_textnodes(text)
        assert result == expected_output, f"Test failed: {result}"



if __name__ == '__main__':
    unittest.main()

