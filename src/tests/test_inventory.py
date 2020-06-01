import unittest
from item import Item
from inventory import Inventory

class TestInventory(unittest.TestCase):
    def test_inventory_load(self):
        items = []
        inventory = Inventory()
        inventory.loadInventory("../inventory.txt")

        file = open("../inventory.txt", "r")

        for line in file:
            # print(line)
            item = line.split(": ")
            name = item[0]
            itemInfo = item[1].split(", ")
            # print("regularPrice: " + str(itemInfo[1][1:]))
            # print("memberPrice: " + str(itemInfo[2][1:]))
            items.append(Item(name, int(itemInfo[0]), float(itemInfo[1][1:]), float(itemInfo[2][1:]),
                                   itemInfo[3].replace("\n", "")))

        file.close()

        self.assertEqual(items, inventory.items)
