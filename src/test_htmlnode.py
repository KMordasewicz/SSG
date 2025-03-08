from typing import override
import unittest

from htmlnode import (
    HTMLNode,
    LeafNode,
    ParentNode
)


class TestHTMLNode(unittest.TestCase):
    @override
    @classmethod
    def setUpClass(cls):
        cls.child_node1: HTMLNode = HTMLNode(tag="ChildA", value="Child node A")
        cls.child_node2: HTMLNode = HTMLNode(tag="ChildB", value="Child node B")
        cls.html_node: HTMLNode = HTMLNode(
            tag="tagA",
            value="This is a test",
            children=[cls.child_node1, cls.child_node2],
            props={
                "href": "https://www.site.com",
                "target": "_blank"
            }
        )


    def test_init(self):
        html_node = HTMLNode()

        self.assertEqual(
            (html_node.tag, html_node.value, html_node.children, html_node.props),
            (None, None, None, None)
        )
        self.assertEqual((
                self.html_node.tag,
                self.html_node.value,
                self.html_node.children,
                self.html_node.props
            ), (
                "tagA",
                "This is a test",
                [self.child_node1, self.child_node2],
                {"href": "https://www.site.com", "target": "_blank"}
            )
        )


    def test_to_html(self) -> None:
        with self.assertRaises(NotImplementedError):
            _ = self.html_node.to_html()


    def test_props_to_html_empty(self) -> None:
        html_node = HTMLNode("a", "b")

        self.assertEqual(html_node.props_to_html(), "")


    def test_props_to_html(self) -> None:
        html_props = self.html_node.props_to_html()
        expected_html_props = ' href="https://www.site.com" target="_blank"'

        self.assertEqual(html_props, expected_html_props)


    def test_repr(self) -> None:
        html_string = str(self.html_node)
        expected_html_string = "HTMLNode(tagA, This is a test, [HTMLNode(ChildA, Child node A, None, None), HTMLNode(ChildB, Child node B, None, None)], {'href': 'https://www.site.com', 'target': '_blank'})"

        self.assertEqual(html_string, expected_html_string)


class TestLeafNode(unittest.TestCase):
    def test_init(self):
        leaf = LeafNode("tagA", "It's a leaf node!", {"a": "b"})
        
        self.assertEqual(
            (leaf.tag, leaf.value, leaf.props, leaf.children),
            ("tagA", "It's a leaf node!", {"a": "b"}, None)
        )


    def test_leaf_to_html_no_value(self):
        leaf = LeafNode("b", None)  # pyright: ignore[reportArgumentType]
        with self.assertRaises(ValueError, msg="All leaf nodes must have a value"):
            _ = leaf.to_html()


    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")


    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        expected_html = "<a href=\"https://www.google.com\">Click me!</a>"

        self.assertEqual(node.to_html(), expected_html)


class TestParentNode(unittest.TestCase):
    def test_init(self):
        child: LeafNode = LeafNode("a", "child")
        pnode: ParentNode = ParentNode(
            "div",
            [child],
            {"href": "https://wwww.google.com"}
        )

        self.assertEqual(
            (pnode.tag, pnode.children, pnode.props, pnode.value),
            (
                "div",
                [child],
                {"href": "https://wwww.google.com"},
                None
            )
        )


    def test_to_html_no_tag(self):
        with self.assertRaises(ValueError, msg="All parent nodes must have a tag"):
            _ = ParentNode(None, [LeafNode("a", "test")]).to_html()  # pyright: ignore[reportArgumentType]


    def test_to_html_no_children(self):
        with self.assertRaises(ValueError, msg="All parent nodes must have a children"):
            _ = ParentNode("div", None).to_html()  # pyright: ignore[reportArgumentType]


    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")


    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )


    def test_to_html_with_grandchildrens(self):
        grandchild_node1 = LeafNode("b", "grandchild1")
        grandchild_node2 = LeafNode("a", "grandchild2")
        grandchild_node3 = LeafNode("c", "grandchild3")
        child_node1 = ParentNode("span", [grandchild_node1], {"elden": "ring"})
        child_node2 = ParentNode("i", [grandchild_node2, grandchild_node3])
        parent_node = ParentNode("div", [child_node1, child_node2])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span elden=\"ring\"><b>grandchild1</b></span><i><a>grandchild2</a><c>grandchild3</c></i></div>",
        )

if __name__ == "__main__":
    _ = unittest.main()
