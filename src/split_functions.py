from textnode import TextNode, TextType
from extract_markdown import extract_markdown_images, extract_markdown_links

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    
    # Iterate over each node in the old nodes list
    for node in old_nodes:
        if node.text_type == TextType.TEXT:
            parts = []
            buffer = ""
            inside_delimited = False

            if not delimiter:
                raise ValueError("Delimiter cannot be empty")
            # Go through each character to handle nested scenarios
            index = 0
            while index < len(node.text):
                if node.text[index:index+len(delimiter)] == delimiter:
                    if inside_delimited:
                        # Before ending a delimited section, check if buffer has content
                        if not buffer.strip():
                            raise ValueError("Empty content between delimiters")
                        parts.append(TextNode(buffer, text_type))
                        buffer = ""
                    else:
                        # Start of a delimited section
                        if buffer:
                            parts.append(TextNode(buffer, TextType.TEXT))
                            buffer = ""
                    # Toggle the delimited state after processing the delimiter
                    inside_delimited = not inside_delimited
                    index += len(delimiter) - 1
                else:
                    buffer += node.text[index]
                index += 1
            if inside_delimited:
                raise ValueError("Invalid Markdown")
            
            # Any remaining text
            if buffer:
                parts.append(TextNode(buffer, TextType.TEXT if not inside_delimited else text_type))
            
            new_nodes.extend(parts)
        else:
            new_nodes.append(node)
        
    return new_nodes

def split_nodes_image(old_nodes):
    new_nodes = []

    for node in old_nodes:
        images = extract_markdown_images(node.text)
        if not images:
            new_nodes.append(node)
        else:
            for alt, url in images:
                split_sections = node.text.split(f"![{alt}]({url})", 1)
                if split_sections[0] != "":
                    new_nodes.append(TextNode(split_sections[0], TextType.TEXT))
                
                new_nodes.append(TextNode(alt, TextType.IMAGE, url))

                remaining_text = split_sections[1]
                while True:
                    next_images = extract_markdown_images(remaining_text)
                    if not next_images:
                        break

                    next_alt, next_url = next_images[0]

                    split_sections = remaining_text.split(f"![{next_alt}]({next_url})", 1)
                    if split_sections[0] != "":
                        new_nodes.append(TextNode(split_sections[0], TextType.TEXT))
                    
                    new_nodes.append(TextNode(next_alt, TextType.IMAGE, next_url))
                    remaining_text = split_sections[1]

                if remaining_text != "":
                    new_nodes.append(TextNode(remaining_text, TextType.TEXT))

    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []

    for node in old_nodes:
        links = extract_markdown_links(node.text)
        if not links:
            new_nodes.append(node)
        else:
            for alt, url in links:
                split_sections = node.text.split(f"[{alt}]({url})", 1)
                if split_sections[0] != "":
                    new_nodes.append(TextNode(split_sections[0], TextType.TEXT))
                
                new_nodes.append(TextNode(alt, TextType.LINK, url))

                remaining_text = split_sections[1]
                while True:
                    next_links = extract_markdown_links(remaining_text)
                    if not next_links:
                        break

                    next_alt, next_url = next_links[0]

                    split_sections = remaining_text.split(f"[{next_alt}]({next_url})", 1)
                    if split_sections[0] != "":
                        new_nodes.append(TextNode(split_sections[0],TextType.TEXT))

                    new_nodes.append(TextNode(next_alt, TextType.LINK, next_url))
                    remaining_text = split_sections[1]

                if remaining_text != "":
                    new_nodes.append(TextNode(remaining_text, TextType.TEXT))

    return new_nodes


def text_to_textnodes(text):
    if not text:
        return []

    initial_nodes = [TextNode(text, TextType.TEXT)]

    nodes_after_images = split_nodes_image(initial_nodes)

    nodes_after_links = split_nodes_link(nodes_after_images)

    nodes_after_bold = split_nodes_delimiter(nodes_after_links, '**', TextType.BOLD)
    nodes_after_italic = split_nodes_delimiter(nodes_after_bold, '*', TextType.ITALIC)
    final_nodes = split_nodes_delimiter(nodes_after_italic, '`', TextType.CODE)

    return final_nodes