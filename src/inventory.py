from item import Item

# Program Constants
INVENTORY_FILE = "inventory.txt"

class Inventory:
    def __init__(self):
        self.items = [] # inventory is a collection of items
        self.loadInventory() # loads items when instance is created

    # Loads inventory into object
    def loadInventory(self):
        file = open(INVENTORY_FILE, "r")

        for line in file:
            # print(line)
            item = line.split(": ")
            name = item[0]
            itemInfo = item[1].split(", ")
            # print("regularPrice: " + str(itemInfo[1][1:]))
            # print("memberPrice: " + str(itemInfo[2][1:]))
            self.items.append(Item(name, int(itemInfo[0]), float(itemInfo[1][1:]), float(itemInfo[2][1:]), itemInfo[3].replace("\n", "")))

    # updates items quantity after checkout
    def updateInventory(self, item):
        if isinstance(item, Item):
            for i in self.items:
                if item.name == i.name:
                    i.qnty = i.qnty - item.qnty
        else:
            raise TypeError("Item should be of type Item()!")