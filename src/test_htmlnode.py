import unittest
from htmlnode import HTMLNode, LeafNode

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
