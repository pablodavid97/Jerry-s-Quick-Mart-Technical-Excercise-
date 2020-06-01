import unittest
from item import Item

class TestItem(unittest.TestCase):
    def test_values(self):
        item = Item()

        # tests for quantities
        with self.assertRaises(TypeError):
            item.qnty = -2

        with self.assertRaises(TypeError):
            item.qnty = "Number"

        with self.assertRaises(TypeError):
            item.qnty = 2.5

        # test for regular price
        with self.assertRaises(TypeError):
            item.regularPrice = -2.6

        with self.assertRaises(TypeError):
            item.regularPrice = "Price"

        # test for member price
        with self.assertRaises(TypeError):
            item.memberPrice = -2.6

        with self.assertRaises(TypeError):
            item.memberPrice = "Price"