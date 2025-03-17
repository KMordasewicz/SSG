import re
from enum import Enum


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNOLIST = "unordered_list"
    OLIST = "ordered_list"


def block_to_block_type(block: str) -> BlockType:
    if re.search(r"^#+ ", block):
        return BlockType.HEADING
    elif block.startswith("```") and block.endswith("```"):
        return BlockType.CODE
    elif block.startswith(">"):
        return BlockType.QUOTE
    elif block.startswith("- "):
        return BlockType.UNOLIST
    elif block.startswith("1. "):
        return BlockType.OLIST
    else:
        return BlockType.PARAGRAPH
