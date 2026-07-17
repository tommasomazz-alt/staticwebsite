class HTMLNode:
    def __init__(
            self, 
            tag: str | None = None, 
            value: str | None = None, 
            children: list["HTMLNode"] | None = None, 
            props: dict[str,str] | None = None
            ) -> None:
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self) -> str:
        raise NotImplementedError("to_html method not implemented")

    def props_to_html(self) -> str:
        if self.props is None:
            return ""
        formatted_props = ""
        for key in self.props:
            formatted_props += f' {key}="{self.props[key]}"'
        return formatted_props

    def __repr__(self) -> str:
        return f"HTMLNode({self.tag}\n,{self.value}\n,{self.children}\n,{self.props})"


class LeafNode(HTMLNode):
    def __init__(
            self,
            tag: str | None,
            value: str,
            props: dict[str, str] | None = None
            ) -> None:
        super().__init__(tag, value, None, props)

    def to_html(self) -> str:
        if not self.value:
            raise ValueError("no value on LeafNode")
        
        if self.tag is None:
            return f"{self.value}"
        
        if self.props is not None:
            formatted_props = self.props_to_html()
            return f"<{self.tag}{formatted_props}>{self.value}</{self.tag}>"

        return f"<{self.tag}>{self.value}</{self.tag}>"
    
    def __repr__(self) -> str:
        return f"HTMLNode({self.tag}\n,{self.value}\n,{self.props})"

