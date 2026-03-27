class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    
    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"
    
    def get_tag(self):
        return self.tag
    
    def get_value(self):
        return self.value
    
    def get_children(self):
        return self.children
    
    def get_props(self):
        return self.props
    
    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        if not self.props:
            return ""
        attributes = ""
        if type(self.props) is dict:
            for attribute in self.props.keys():
                key = attribute
                value = self.props[key]
                attributes += f" {key}=\"{value}\""
        return attributes
    
class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)
    
    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"

    def to_html(self):
        if self.value is None:
            raise ValueError("LeafNode must contain a value")
        if self.tag is None:
            return self.value
        attributes = self.props_to_html()
        return f"<{self.tag}{attributes}>{self.value}</{self.tag}>"

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)
    
    def __repr__(self):
        return f"ParentNode({self.tag}, {self.children}, {self.props})"
    
    def to_html(self):
        if self.tag is None:
            raise ValueError("ParentNode must contain a tag")
        if self.children is None or len(self.children) == 0:
            raise ValueError("ParentNode must have children")
        attributes = self.props_to_html()
        open_tag = f"<{self.tag}{attributes}>"
        close_tag = f"</{self.tag}>"
        content = ""
        for child in self.children:
            if type(child) is LeafNode or type(child) is ParentNode:
                content += child.to_html()
            else:
                raise ValueError("ParentNode children must be LeafNode or ParentNode")
        return open_tag + content + close_tag