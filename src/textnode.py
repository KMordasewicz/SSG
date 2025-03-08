from __future__ import annotations
from enum import Enum
from typing import override

class TextType(Enum):
    NORMAL = ""
    BOLD = "**"
    ITALIC = "_"
    CODE = "`"
    LINK = "[("
    IMAGE = "![("

class TextNode:
    def __init__(self, text: str, text_type: TextType, url: str|None=None) -> None:
        self.text: str = text
        self.text_type: TextType = text_type
        self.url: str|None = url


    @override
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, TextNode):
            return False

        return (
            self.text == other.text
            and self.text_type == other.text_type
            and self.url == other.url
        )


    @override
    def __repr__(self) -> str:
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"
