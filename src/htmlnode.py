
class HtmlNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props if props is not None else {}

    def to_html(self):
        raise NotImplementedError


    def props_to_html(self):
        #Join the lines together, remove any parentheses,
        formatted_props = [f'{key}="{value}"' for key, value in self.props.items()]
        return ' ' + ' '.join(formatted_props) if formatted_props else ''
    
    def __repr__(self):
        return f"HtmlNode(tag={self.tag}, value={self.value}, children={self.children}, props={self.props})"
    

class LeafNode(HtmlNode):
    def __init__(self, tag=None, value=None, props=None):
        super().__init__(tag=tag, value=value, children=None, props=props)
        
        if value is None:
            raise ValueError("LeafNode must have a value.")
        

    def to_html(self):
        # Check for a valid value
        if not self.value:
            raise ValueError("LeafNode must have a value.")

        # If the value of tag is None, return the value as raw text
        if self.tag is None:
            return self.value

        # If there's a tag, render it with props and value
        props_str = self.props_to_html()
        return f"<{self.tag}{props_str}>{self.value}</{self.tag}>"
    

class ParentNode(HtmlNode):
    def __init__(self, tag, children, props=None):

        if not tag:
            raise ValueError("ParentNode must have a tag.")
        
        if not children:
            raise ValueError("ParentNode must have children.")
        super().__init__(tag=tag, value=None, children=children, props=props)

    def to_html(self):
        props_str = self.props_to_html()
        child_html_strings = [child.to_html() for child in self.children]
        children_html = ''.join(child_html_strings)
        return f"<{self.tag}{props_str}>{children_html}</{self.tag}>"
    


    