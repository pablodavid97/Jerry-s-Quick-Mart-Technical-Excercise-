from item import Item

class Inventory:
    def __init__(self):
        self.items = [] # inventory is a collection of items

    def __eq__(self, other):
        return self.items == other.items

    # Loads inventory into object
    def loadInventory(self, filename):
        file = open(filename, "r")

        for line in file:
            # print(line)
            item = line.split(": ")
            name = item[0]
            itemInfo = item[1].split(", ")
            # print("regularPrice: " + str(itemInfo[1][1:]))
            # print("memberPrice: " + str(itemInfo[2][1:]))
            self.items.append(Item(name, int(itemInfo[0]), float(itemInfo[1][1:]), float(itemInfo[2][1:]), itemInfo[3].replace("\n", "")))

        file.close()

    # updates items quantity after checkout
    def updateInventory(self, item):
        if isinstance(item, Item):
            for i in self.items:
                if item.name == i.name:
                    i.qnty = i.qnty - item.qnty
        else:
            raise TypeError("Item should be of type Item()!")