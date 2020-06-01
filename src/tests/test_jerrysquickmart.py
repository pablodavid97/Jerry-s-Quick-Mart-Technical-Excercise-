import unittest
from jerrysquickmart import JerrysQuickMart

class TestJerrysQuickMart(unittest.TestCase):

    def test_user_inputs(self):
        jm = JerrysQuickMart()

        # Testing main menu option
        with self.assertRaises(TypeError):
            jm.menuOption = "Number"

        with self.assertRaises(ValueError):
            jm.menuOption = 4

        # testing transaction menu option
        with self.assertRaises(TypeError):
            jm.transactionOption = "Number"

        with self.assertRaises(ValueError):
            jm.transactionOption = 0

        # testing customer selection option
        with self.assertRaises(TypeError):
            jm.customerOption = 34

        with self.assertRaises(ValueError):
            jm.customerOption = "option"

        # testing add item option
        with self.assertRaises(ValueError):
            jm.addInput = ["name", "item", "error"]

        with self.assertRaises(TypeError):
            jm.addInput = [23, "Number"]

        with self.assertRaises(ValueError):
            jm.addInput = ["item", -5]

        # testing remove item option
        with self.assertRaises(TypeError):
            jm.rmvOption = "Invalid option"

        with self.assertRaises(ValueError):
            jm.rmvOption = 4

        # testing cash amount
        with self.assertRaises(TypeError):
            jm.cashAmount = "Number"