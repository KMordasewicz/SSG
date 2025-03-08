import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)

        self.assertEqual(node, node2)
        self.assertEqual(node.url, None)


    def test_neq(self):
        node1 = TextNode("Node 1", TextType.ITALIC, "https://google.com")
        node2 = TextNode("Node 2", TextType.ITALIC, "https://google.com")
        node3 = TextNode("Node 1", TextType.BOLD, "https://google.com")
        node4 = TextNode("Node 1", TextType.ITALIC, "https://duckduckgo.com")
        not_node = "NotNode 1"

        self.assertNotEqual(node1, node2)
        self.assertNotEqual(node1, node3)
        self.assertNotEqual(node1, node4)
        self.assertNotEqual(node1, not_node)


if __name__ == "__main__":
    unittest.main()
