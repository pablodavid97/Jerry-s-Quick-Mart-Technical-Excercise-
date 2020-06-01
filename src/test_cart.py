import unittest
from item import Item
from cart import Cart

class CartTest(unittest.TestCase):
    def test_add_item_to_cart(self):
        item = Item()
        cart = Cart()
        cart.addItem(item)
        with self.assertRaises(ValueError):
            cart.addItem(item)

    def test_remove_item_from_cart(self):
        cart = Cart()
        with self.assertRaises(TypeError):
            cart.removeItem(2)

        with self.assertRaises(ValueError):
            cart.removeItem("This item does not exist")