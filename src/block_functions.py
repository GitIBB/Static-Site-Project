from htmlnode import HtmlNode, ParentNode, LeafNode
from textnode import TextType, TextNode, text_node_to_html_node
from split_functions import text_to_textnodes


def markdown_to_blocks(markdown):
    # Splitting the markdown into blocks
    blocks = markdown.split('\n\n')

    # Clean the blocks by splitting the blocks with a newline,
    # then stripping the lines, joining them back together and then stripping them again,
    # to get rid of any leading / trailing whitespace and redundant newlines
    cleaned_blocks = [
        '\n'.join(line.strip() for line in block.split('\n')).strip()
        for block in blocks if block.strip() != ""
                    ]
    return cleaned_blocks


def is_valid_heading_line(line):
    hashtag_count = 0   
    if line.startswith("#"):
        for char in line:
            if char == '#':
                hashtag_count += 1
            else:
                break
        if hashtag_count > 0 and hashtag_count <= 6 and line[hashtag_count] == " ":
            return True
        
    return False

def block_to_block_type(block):

    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"
    PARAGRAPH = "paragraph"
    
    lines = block.split('\n')

    if len(lines) == 1 and is_valid_heading_line(lines[0]):
        return HEADING
    
    if block.startswith("```"):
        if block.endswith("```"):
            return CODE

    all_lines_are_quotes = all(line.startswith(">") for line in lines)
    if all_lines_are_quotes:
        return QUOTE
    
    if (block.startswith("*") and block[1] == " ") or (block.startswith("-") and block[1] == " "):
        return UNORDERED_LIST
    
    number = 1
    all_lines_valid = True

    for line in lines:
        expected_start = f"{number}. " # the start should be a number followed by a period followed by a space. 
        if not line.startswith(expected_start):
            all_lines_valid = False
            break
        number += 1

    if all_lines_valid and number > 1:
        return ORDERED_LIST 

    return PARAGRAPH

            
def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    converted_nodes = []

    for block in blocks:
        converted_block = create_htmlnode_from_block(block)
        converted_nodes.append(converted_block)

    root_node = ParentNode("div", converted_nodes)

    return root_node

def text_to_quote_children(text):
    lines = text.strip().split('\n')
    return [LeafNode("p", line.lstrip('> ').strip()) for line in lines]

def text_to_list_children(text, list_type):
    lines = text.strip().split('\n')
    return [LeafNode("li", line.strip('- ').strip()) for line in lines if line.strip()]

def text_to_code_children(text):
    lines = text.strip().split('\n')
    if lines and lines[0].startswith('```') and lines[-1].startswith('```'):
        clean_lines = lines[1:-1]
    else:
        clean_lines = lines
    return clean_lines

def text_to_children(text):
    # use function to parse text into TextNode objects
    text_nodes = text_to_textnodes(text)

    # Convert each TextNode into a HtmlNode
    return [text_node_to_html_node(text_node) for text_node in text_nodes]


def create_htmlnode_from_block(block):
    block_type = block_to_block_type(block)

    if block_type == "heading":
            hashtag_count = 0
            for char in block:
                if char == '#':
                    hashtag_count += 1
                else:
                    break
            heading_level = f"h{hashtag_count}"
            heading_text = block[hashtag_count:].strip()
            node = LeafNode(f"{heading_level}", heading_text)
        # If dealing with multiple heading nodes, combine them

    elif block_type == "code":
        clean_lines = text_to_code_children(block) # Strip any surrounding whitespace or newlines
        code_text = '\n'.join(clean_lines)
        if not code_text:
            raise ValueError("No code content found in block.")
        code_node = LeafNode("code", code_text)
        node = ParentNode("pre", [code_node])

    elif block_type == "quote":
        children = text_to_quote_children(block)
        node = ParentNode("blockquote", children)

    elif block_type == "unordered_list":
        children = text_to_list_children(block, "unordered")
        node = ParentNode("ul", children)

    elif block_type == "ordered_list":
        children = text_to_list_children(block, "ordered")
        node = ParentNode("ol", children)

    elif block_type == "paragraph":
        node = LeafNode("p", block.strip())

    return node



    
