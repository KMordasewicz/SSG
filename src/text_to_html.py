from collections.abc import Iterator
import re
from itertools import chain, zip_longest
from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode, ParentNode
from blocknode import BlockType, block_to_block_type


def text_node_to_html_node(text_node: TextNode) -> LeafNode:
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            if not text_node.url:
                raise ValueError("Links needs URL")
            return LeafNode("a", text_node.text, {"href": text_node.url})
        case TextType.IMAGE:
            if not text_node.url:
                raise ValueError("Image needs src URL")
            return LeafNode("img", "", {
                "src": text_node.url,
                "alt": text_node.text
            })


def split_node_delimiter(
    old_node: list[TextNode],
    delimiter: str,
    text_type: TextType
) -> list[TextNode]:
    new_nodes: list[TextNode] = []
    for node in old_node:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        text_sections = node.text.split(delimiter)
        if len(text_sections) == 1:
            new_nodes.append(node)
            continue
        if not len(text_sections) == 3:
            message = f"Invalid Markdown syntax, delimiter: {delimiter}" \
            + f" should have a closing pair in: {text_sections[1]}"
            raise Exception(message)
        new_node = [
            TextNode(text_sections[0], node.text_type),
            TextNode(text_sections[1], text_type),
            TextNode(text_sections[2], node.text_type)
        ]
        new_node = list(filter(lambda node: node.text != "", new_node))
        new_nodes.extend(new_node)

    return new_nodes


def extract_markdown_images(text: str) -> list[tuple[str, str]|None]:
    regex = r"(?:.*?!\[(.*?)\]\((.*?)\).*?)+?"
    matches = re.findall(regex, text)

    return matches


def extract_markdown_links(text: str) -> list[tuple[str, str]|None]:
    regex = r"(?:.*?(?<!!)\[(.*?)\]\((.*?)\).*?)+?"
    matches = re.findall(regex, text)

    return matches


def split_nodes_image(
    old_node: list[TextNode],
) -> list[TextNode]:
    new_nodes: list[TextNode] = []
    for node in old_node:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        regex_split = r"!\[.*?\]\(.*?\)"
        text_sections = re.split(regex_split, node.text)
        if len(text_sections) == 1:
            new_nodes.append(node)
            continue
        images = extract_markdown_images(node.text)
        new_node: list[TextNode] = []
        text_image_combo: Iterator[str|tuple[str, str]|None] = chain.from_iterable(zip_longest(text_sections, images))
        for node in text_image_combo:
            if not node:
                continue
            if isinstance(node, str):
                new_node.append(TextNode(node, TextType.TEXT))
            else:
                new_node.append(TextNode(node[0], TextType.IMAGE, node[1]))
        new_nodes.extend(new_node)

    return new_nodes


def split_nodes_link(
    old_node: list[TextNode],
) -> list[TextNode]:
    new_nodes: list[TextNode] = []
    for node in old_node:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        regex_split = r"(?<!!)\[.*?\]\(.*?\)"
        text_sections = re.split(regex_split, node.text)
        if len(text_sections) == 1:
            new_nodes.append(node)
            continue
        images = extract_markdown_links(node.text)
        new_node: list[TextNode] = []
        text_link_combo: Iterator[str|tuple[str, str]|None] = chain.from_iterable(zip_longest(text_sections, images))
        for node in text_link_combo:
            if not node:
                continue
            if isinstance(node, str):
                new_node.append(TextNode(node, TextType.TEXT))
            else:
                new_node.append(TextNode(node[0], TextType.LINK, node[1]))
        new_nodes.extend(new_node)

    return new_nodes


def text_to_textnodes(text: str) -> list[TextNode]:
    new_node = split_node_delimiter(
        split_node_delimiter(
            split_node_delimiter(
                split_nodes_image(
                    split_nodes_link(
                        [TextNode(text, TextType.TEXT)]
                    )
                ),
                "**",
                TextType.BOLD
            ),
            "_",
            TextType.ITALIC
        ),
        "`",
        TextType.CODE
    )

    return new_node


def markdown_to_blocks(markdown: str) -> list[str]:
    blocks: list[str] = list(
        filter(lambda x: x != "",
               map(lambda x: x.strip(), markdown.split("\n\n"))
        )
    )

    return blocks


def text_to_children(text: str) -> list[LeafNode]:
    return list(map(text_node_to_html_node, text_to_textnodes(text)))


def markdown_list_to_text(block: str) -> list[str]:
    points = block.splitlines()

    return list(map(lambda x: x.split(maxsplit=1)[1], points))


def code_block_to_html(text: str) -> ParentNode:
    code_content = re.split(r"\n?```\n?", text)[1] + "\n"
    return ParentNode("pre", [LeafNode("code", code_content)])


def heading_block_to_html(text: str) -> ParentNode:
    text_elm = text.split(maxsplit=1)
    hashes = text_elm[0].count("#")
    children = text_to_children(text_elm[1])
    if 1 <= hashes <= 6:
            return ParentNode(f"h{hashes}", children)
    else:
        raise ValueError(f"Heading markdown should contain 1-6 '#', provided {hashes}'.")


def quote_block_to_html(text: str) -> ParentNode:
    quotes = text.splitlines()
    quotes_content = list(map(lambda x: x.split(">", maxsplit=1)[1], quotes))
    content_block =  " ".join(quotes_content)
    children = text_to_children(content_block)

    return ParentNode("blockquote", children)


def list_block_to_html(text: str, tag: str) -> ParentNode:
    points = markdown_list_to_text(text)
    node_points = map(lambda x: text_to_children(x), points)
    parent_points = list(map(lambda x: ParentNode("li", x), node_points))

    return ParentNode(tag, parent_points)


def paragraph_block_to_html(text: str) -> ParentNode:
    text_lines = text.splitlines()
    text_line = " ".join(text_lines)
    children = text_to_children(text_line)

    return ParentNode("p", children)


def block_to_html_parent_node(block_type: BlockType, text: str) -> ParentNode:
    match block_type:
        case BlockType.CODE:
            return code_block_to_html(text)
        case BlockType.HEADING:
            return heading_block_to_html(text)
        case BlockType.QUOTE:
            return quote_block_to_html(text)
        case BlockType.UNOLIST:
            return list_block_to_html(text, "ul")
        case BlockType.OLIST:
            return list_block_to_html(text, "ol")
        case BlockType.PARAGRAPH:
            return paragraph_block_to_html(text)


def markdown_to_html_node(markdown: str) -> ParentNode:
    blocks = markdown_to_blocks(markdown)
    child_nodes: list[HTMLNode] = []
    for block in blocks:
        block_type = block_to_block_type(block)
        child_nodes.append(block_to_html_parent_node(block_type, block))

    return ParentNode("div", child_nodes)







