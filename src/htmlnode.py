class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    
    def __repr__(self):
        attributes = self.props_to_html()
        if self.value:
            return f"<{self.tag}{attributes}>{self.value}</{self.tag}>"
        if self.children:
            return f"<{self.tag}{attributes}>{self.children}</{self.tag}>"
        else:
            return f"<{self.tag}{attributes}>"
    
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