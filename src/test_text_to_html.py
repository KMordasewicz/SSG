import unittest

from text_to_html import text_node_to_html_node
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
        with self.assertRaises(ValueError, msg="Links needs URL"):
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
        with self.assertRaises(ValueError, msg="Image needs src URL"):
            html_node: LeafNode = text_node_to_html_node(node)
