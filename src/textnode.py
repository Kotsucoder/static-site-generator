from enum import Enum


class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALICS = "italics"
    CODEBLOCK = "code"
    HYPERLINK = "link"
    IMAGE = "image"


class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        if type(other) is TextNode:
            sametext = self.text == other.get_text()
            sametype = self.text_type == other.get_type()
            sameurl = self.url == other.get_url()
        else:
            return NotImplemented
        return sametext and sametype and sameurl
    
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"
    
    def get_text(self):
        return self.text
    
    def get_type(self):
        return self.text_type
    
    def get_url(self):
        return self.url