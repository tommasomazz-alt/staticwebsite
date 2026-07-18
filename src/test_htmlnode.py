import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):
    def test_props_onepair(self):
        node = HTMLNode("HTML","valore",["lista"],{"io":"dizionario"} )
        result = node.props_to_html()
        self.assertEqual(result,' io="dizionario"')
        print(result)

    def test_props_twopairs(self):
        node = HTMLNode("HTML","valore",["lista"],{"io":"dizionario","href":"link.it"} )
        result = node.props_to_html()
        self.assertEqual(result,' io="dizionario" href="link.it"')
        print(result)

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
    
    def test_leaf_to_html_props(self):
        node = LeafNode("a","Linkami",{"href":"greenland.com"})
        self.assertEqual(node.to_html(),'<a href="greenland.com">Linkami</a>')
    
    def test_leaf_to_html_no_tag(self):
        node = LeafNode(None,"ciao mamma")
        self.assertEqual(node.to_html(),"ciao mamma")
    
    def test_value_missing_leaf_error(self):
        node = LeafNode("a",None)
        with self.assertRaises(ValueError):
            node.to_html()

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

    def test_to_html_with_no_children_None(self):
        parent_node = ParentNode("div",None)
        with self.assertRaises(ValueError):
            parent_node.to_html()

    def test_to_html_with_no_children_empty(self):
        parent_node = ParentNode("div",[])
        with self.assertRaises(ValueError):
            parent_node.to_html()

    def test_to_html_with_subparents_and_props(self):
        grandchild_node = LeafNode("b", "grandchild",{"href":"link.it"})
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node],{"prop":"ciao"})
        self.assertEqual(
            parent_node.to_html(),
            '<div prop="ciao"><span><b href="link.it">grandchild</b></span></div>',
        )
