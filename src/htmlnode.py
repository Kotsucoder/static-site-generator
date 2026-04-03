"""
This module provides objects that should be used for representing and working with HTML syntax
parsing. These objects provide a semantic representation of the syntax to make it easier to manage
the raw text in a clear, defined data structure.

Classes:
    HTMLNode: The basic template for HTML objects.
    LeafNode(HTMLNode): Extends HTMLNode to represent HTML objects with content, but no children.
    ParentNode(HTMLNode): Extends HTMLNode to represent HTML objects with children, but no content.
"""


from typing import Optional, Sequence


class HTMLNode:
    """
    Semantically represents HTML syntax into an object which provides a clear structure
    to more easily manage arbitrary HTML text.

    Attributes:
        tag: String representing the HTML tag.
        value: String representing the contents of the element.
        children: List of HTMLNode objects contained within this HTMLNode.
        props: Dictionary of attributes with String keys representing the attribute's name, and String values for the contents.

    Functions:
        to_html: Not implemented in this class.
        props_to_html: Converts the props attribute to a string of HTML attributes in the proper HTML syntax.
    """


    def __init__(self, tag:Optional[str]=None, value:Optional[str]=None, children:Optional[Sequence['HTMLNode']]=None, props:Optional[dict[str,str]]=None) -> None:
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    
    def __repr__(self) -> str:
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"
    
    def to_html(self) -> str:
        """
        Converts the HTML object into a String providing it's proper HTML syntax.
        This function is not implemented in this class. Please use one of its child classes.
        """
        raise NotImplementedError
    
    def props_to_html(self) -> str:
        """
        Converts the props attribute of this class to a String representation of the HTML attributes
        in proper HTML syntax.
        """
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
    """
    Semantically represents HTML syntax into an object which provides a clear structure
    to more easily manage arbitrary HTML text. LeafNodes have a value but no children.

    Attributes:
        tag: String representing the HTML tag.
        value: String representing the contents of the element.
        props: Dictionary of attributes with String keys representing the attribute's name, and String values for the contents.

    Functions:
        to_html: Converts the HTML object into a String providing it's proper HTML syntax.
        props_to_html: Converts the props attribute to a string of HTML attributes in the proper HTML syntax.
    """


    def __init__(self, tag:Optional[str], value:Optional[str], props:Optional[dict[str,str]]=None):
        super().__init__(tag, value, None, props)
    
    def __repr__(self) -> str:
        return f"LeafNode({self.tag}, {self.value}, {self.props})"

    def to_html(self) -> str:
        """
        Converts the HTML object into a String providing it's proper HTML syntax.
        """
        if self.tag is None and self.value is not None:
            return self.value
        if self.tag is None and self.value is None:
            raise ValueError("element must have either a tag or a value")
        attributes = self.props_to_html()
        if self.value is None:
            return f"<{self.tag}{attributes}>"
        return f"<{self.tag}{attributes}>{self.value}</{self.tag}>"


class ParentNode(HTMLNode):
    children: list
    """
    Semantically represents HTML syntax into an object which provides a clear structure
    to more easily manage arbitrary HTML text. ParentNodes have children and no value.

    Attributes:
        tag: String representing the HTML tag.
        children: List of HTMLNode objects contained within this HTMLNode.
        props: Dictionary of attributes with String keys representing the attribute's name, and String values for the contents.

    Functions:
        to_html: Converts the HTML object into a String providing it's proper HTML syntax.
        props_to_html: Converts the props attribute to a string of HTML attributes in the proper HTML syntax.
    """


    def __init__(self, tag: str, children: Sequence[HTMLNode], props:Optional[dict[str,str]]=None):
        super().__init__(tag, None, children, props)
    
    def __repr__(self) -> str:
        return f"ParentNode({self.tag}, {self.children}, {self.props})"
    
    def to_html(self) -> str:
        """
        Converts the HTML object into a String providing it's proper HTML syntax.
        """
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