import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


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

class TestParentNode(unittest.TestCase):
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
    
    def test_to_html_no_children_error_expected(self):
        parent_node = ParentNode("a", [], {"href": "https://somesome.some"})
        with self.assertRaises(ValueError) as context:
            parent_node.to_html()
    
    def test_to_html_many_children(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold Text"),
                LeafNode("i", "Italic Text"),
                LeafNode("a", "Click Me!", {"href": "https://somesome.some"}),
                LeafNode(None, "Just Text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            '<p><b>Bold Text</b><i>Italic Text</i><a href="https://somesome.some">Click Me!</a>Just Text</p>'
        )

    

if __name__ == "__main__":
    unittest.main()