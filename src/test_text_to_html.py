import unittest

from text_to_html import (
    split_nodes_link,
    text_node_to_html_node,
    split_node_delimiter,
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_image,
    text_to_textnodes,
    markdown_to_blocks
)
from textnode import TextNode, TextType
from htmlnode import LeafNode


class TestTextToHTML(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node: LeafNode = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")


    def test_bold(self):
        node = TextNode("This is a bold text node", TextType.BOLD)
        html_node: LeafNode = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a bold text node")


    def test_italic(self):
        node = TextNode("This is a italic text node", TextType.ITALIC)
        html_node: LeafNode = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is a italic text node")


    def test_code(self):
        node = TextNode("love = you + me", TextType.CODE)
        html_node: LeafNode = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "love = you + me")


    def test_link_good(self):
        node = TextNode("This is a link node", TextType.LINK, "https://www.google.com")
        html_node: LeafNode = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is a link node")
        self.assertEqual(html_node.props, {
            "href": "https://www.google.com"
        })


    def test_link_bad(self):
        node = TextNode("This is a link node", TextType.LINK)
        with self.assertRaisesRegex(ValueError, "Links needs URL"):
            html_node: LeafNode = text_node_to_html_node(node)


    def test_image_good(self):
        node = TextNode("This is a image node", TextType.IMAGE, "~/usr/you/picture.jpg")
        html_node: LeafNode = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props, {
            "src": "~/usr/you/picture.jpg",
            "alt": "This is a image node"
        })


    def test_image_bad(self):
        node = TextNode("This is a link node", TextType.IMAGE)
        with self.assertRaisesRegex(ValueError, "Image needs src URL"):
            html_node: LeafNode = text_node_to_html_node(node)


class TestSplitNodeDelimiter(unittest.TestCase):
    def test_good_code(self):
        text_node = TextNode("This code is based: `Bitcoin.mineAll()`", TextType.TEXT)
        expected = [
            TextNode("This code is based: ", TextType.TEXT),
            TextNode("Bitcoin.mineAll()", TextType.CODE)
        ]
        result = split_node_delimiter([text_node], "`", TextType.CODE)

        self.assertEqual(result, expected)


    def test_good_bold(self):
        text_node = TextNode("This text is **bold**, very BOLD!", TextType.TEXT)
        expected = [
            TextNode("This text is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(", very BOLD!", TextType.TEXT)
        ]
        result = split_node_delimiter([text_node], "**", TextType.BOLD)

        self.assertEqual(result, expected)


    def test_bad(self):
        text_node = TextNode("This is _incorrect text", TextType.TEXT)
        message = f"Invalid Markdown syntax, delimiter: _" \
        + f" should have a closing pair in: incorrect text"

        with self.assertRaisesRegex(Exception, message):
            _ = split_node_delimiter([text_node], "_", TextType.ITALIC)


    def test_skip(self):
        text_nodes = [
            TextNode("Text _node_ 1",TextType.ITALIC),
            TextNode("Text node 2", TextType.TEXT)
        ]
        result = split_node_delimiter(text_nodes, "_", TextType.ITALIC)

        self.assertEqual(result, text_nodes)


class TestExtractMarkdownImages(unittest.TestCase):
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)


    def test_extract_markdown_images_mult(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and also this ![image2](https://i.imgur.com/abdcaDe.png)"
        )
        self.assertListEqual([
            ("image", "https://i.imgur.com/zjjcJKZ.png"),
            ("image2","https://i.imgur.com/abdcaDe.png")
        ], matches)


    def test_extract_markdown_images_no_match(self):
        matches = extract_markdown_images(
            "This is text with an [link](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([], matches)


class TestExtractMarkdownLinks(unittest.TestCase):
    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with an [link](https://www.google.com)"
        )
        self.assertListEqual([("link", "https://www.google.com")], matches)


    def test_extract_markdown_links_mult(self):
        matches = extract_markdown_links(
            "This is text with an [link](https://www.google.com) and also this [link2](https://www.wikipedia.com)"
        )
        self.assertListEqual([
            ("link", "https://www.google.com"),
            ("link2","https://www.wikipedia.com")
        ], matches)


    def test_extract_markdown_links_no_match(self):
        matches = extract_markdown_links(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([], matches)


class TestSplitNodeImage(unittest.TestCase):
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )


    def test_split_image(self):
        node = TextNode(
            "This is text with an [image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an [image](https://i.imgur.com/zjjcJKZ.png) and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                )
            ],
            new_nodes,
        )


    def test_split_no_image(self):
        node = TextNode(
            "This is text with an [image](https://i.imgur.com/zjjcJKZ.png) and another [second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an [image](https://i.imgur.com/zjjcJKZ.png) and another [second image](https://i.imgur.com/3elNhQu.png)", TextType.TEXT)
            ],
            new_nodes,
        )


class TestSplitNodeLink(unittest.TestCase):
    def test_split_links(self):
        node = TextNode(
            "This is text with an [link](https://www.google.com) and another [second link](https://www.wikipedia.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://www.google.com"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second link", TextType.LINK, "https://www.wikipedia.com"
                ),
            ],
            new_nodes,
        )


    def test_split_link(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another [link](https://www.wikipedia.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://www.wikipedia.com")
            ],
            new_nodes,
        )


    def test_split_no_link(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)", TextType.TEXT)
            ],
            new_nodes,
        )


class TestTestToTextnodes(unittest.TestCase):
    def test1(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        result = text_to_textnodes(text)

        self.assertEqual(result, expected)


    def test2(self):
        text = "This is text with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        expected = [
            TextNode("This is text with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        result = text_to_textnodes(text)

        self.assertEqual(result, expected)


    def test3(self):
        text = "This is **text** with an _italic_ word and a `code block` and an [obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.LINK, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        result = text_to_textnodes(text)

        self.assertEqual(result, expected)


    def test4(self):
        text = "This is **text** with an italic word and a `code block` and a [link](https://boot.dev)"
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an italic word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        result = text_to_textnodes(text)

        self.assertEqual(result, expected)


class TestMarkdownToBlocks(unittest.TestCase):
    def test_markdown_to_blocks1(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)

        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks2(self):
        md = """
# This is a heading

This is a paragraph of text. It has some **bold** and _italic_ words inside of it.


- This is the first list item in a list block
- This is a list item
- This is another list item

"""
        blocks = markdown_to_blocks(md)

        self.assertEqual(
            blocks,
            [
                "# This is a heading",
                "This is a paragraph of text. It has some **bold** and _italic_ words inside of it.",
                "- This is the first list item in a list block\n- This is a list item\n- This is another list item"
            ]
        )


    def test_markdown_to_blocks_one_line(self):
        md = "This is a sigle line"
        block = markdown_to_blocks(md)

        self.assertEqual(block, [md])


    def test_markdown_to_blocks_no_line(self):
        md = ""
        block = markdown_to_blocks(md)

        self.assertEqual(block, [])

if __name__ == "__main__":
    unittest.main()
