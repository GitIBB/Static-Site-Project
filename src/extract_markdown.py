import re

def extract_markdown_images(text):
    # defines a list of tuples matching the alt text with the url of markdown images
    img_tuples = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return img_tuples

def extract_markdown_links(text):
    # defines a list of tuples matching the anchor text with the url of a link
    link_tuples = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return link_tuples