from __future__ import annotations
from abc import abstractmethod
from collections.abc import Sequence
from functools import reduce
from typing import final, override



class HTMLNode:
    def __init__(
        self,
        tag: str|None=None,
        value: str|None=None,
        children: Sequence[HTMLNode]|None=None,
        props: dict[str, str]|None=None
    ) -> None:
        self.tag: str|None = tag
        self.value: str|None = value
        self.children: Sequence[HTMLNode]|None = children
        self.props: dict[str, str]|None = props


    @abstractmethod
    def to_html(self):  # pyright: ignore[reportUnknownParameterType]
        raise NotImplementedError()


    def props_to_html(self) -> str:
        if not self.props:
            return ""
        return " " + " ".join(map(lambda x: f"{x[0]}=\"{x[1]}\"", self.props.items()))


    @override
    def __repr__(self) -> str:
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"


@final
class LeafNode(HTMLNode):
    def __init__(
        self,
        tag: str|None,
        value: str,
        props: dict[str, str] | None = None
    ) -> None:
        super().__init__(tag, value, None, props)


    @override
    def to_html(self) -> str|Exception:
        if self.value is None:
            raise ValueError("All leaf nodes must have a value")
        elif not self.tag:
            return self.value
        elif self.tag == "img":
            if self.value != "":
                raise ValueError("Image node shouldn't have a value")
            return f"<{self.tag}{self.props_to_html()} />"
        else:
            return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"


class ParentNode(HTMLNode):
    def __init__(
        self,
        tag: str,
        children: Sequence[HTMLNode],
        props: dict[str, str] | None = None
    ) -> None:
        super().__init__(tag, None, children, props)


    @override
    def to_html(self) -> str|Exception:
        if not self.tag:
            raise ValueError("All parent nodes must have a tag")
        elif not self.children:
            raise ValueError("All parent nodes must have a children")
        else:
            children_html = reduce(
                lambda acc, next_node: acc + next_node.to_html(),
                self.children,
                ""
            )
            # accumlator:str = ""
            # for child in self.children:
            #         accumlator += child.to_html()
            return LeafNode(self.tag, children_html, self.props).to_html()





