import unittest

from htmlnode import HTMLNode, LeafNode


class TestHTMLNode(unittest.TestCase):
    def test_props_eq(self):
        new_dict = {
            "href": "https://somesome.some",
            "target": "_blank",
        }
        
        node = HTMLNode(props=new_dict)
        node2 = HTMLNode(props=new_dict)
        self.assertEqual(node, node2)
    
    def test_repr_eq(self):
        node = HTMLNode(
            "div",
            "Hello World!",
            None,
            {"class": "primary"}
        )
        self.assertEqual(
            node.__repr__(),
            "HTMLNode(div, Hello World!, children: None, {'class': 'primary'})",
        )

class TestLeafNode(unittest.TestCase):
    def test_to_html_eq(self):
        node = LeafNode("p", "Hello World!")
        self.assertEqual(node.to_html(), "<p>Hello World!</p>")
    
    def test_repr_eq(self):
        node = LeafNode(
            "div",
            "Hello World!",
            {"class": "primary"}
        )
        self.assertEqual(
            node.__repr__(),
            "LeafNode(div, Hello World!, {'class': 'primary'})",
        )

    def test_to_html_props_eq(self):
        node = LeafNode("a", "This is a nice link!", {"href": "https://somesome.some"})
        self.assertEqual(node.to_html(), '<a href="https://somesome.some">This is a nice link!</a>')
    
    def test_to_html_no_tag(self):
        node = LeafNode(None, "Hello, World!")
        self.assertEqual(node.to_html(), "Hello, World!")

if __name__ == "__main__":
    unittest.main()