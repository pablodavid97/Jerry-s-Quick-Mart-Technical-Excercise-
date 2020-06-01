from item import Item

# Program Constants
REGULAR_CUSTOMER = True
TAX_VALUE = 0.065

class Cart:
    # Cart is a collection of items
    def __init__(self):
        self.items = []
        self.itemNum = 0
        self.subtotal = 0.0
        self.tax = 0.0
        self.total = 0.0
        self.memberSubtotal = 0.0
        self.memberTax = 0.0
        self.memberTotal = 0.0
        self._regularCustomer = REGULAR_CUSTOMER # by default is assumed a regular customer

    @property
    def regularCustomer(self):
        return self._regularCustomer

    @regularCustomer.setter
    def regularCustomer(self, customer):
        self._regularCustomer = customer

    # adds items if not added already (doesn't accept duplicates)
    def addItem(self, item):
        try:
            self.items.index(item)
        except ValueError:
            self.items.append(item)
            self.itemNum += item.qnty

            self.subtotal += item.regularPrice * item.qnty
            self.memberSubtotal += item.memberPrice * item.qnty

            if item.isItemTaxable():
                self.tax += item.regularPrice * item.qnty * TAX_VALUE
                self.memberTax += item.memberPrice * item.qnty * TAX_VALUE

            self.total = self.subtotal + self.tax
            self.memberTotal = self.memberSubtotal + self.memberTax

        raise ValueError("Item already in list!")

    # removes items only if they exist
    def removeItem(self, name):
        if not isinstance(name, str):
            raise TypeError("Item name should be a non-empty string!")

        n = len(self.items)
        item = Item()

        itemExists = False

        for i in range(0, n):
            if self.items[i].name == name:
                item = self.items.pop(i)
                itemExists = True
                break

        if not itemExists:
            raise ValueError("Item is not in cart or doesn't exist, make sure you typed the name correctly!")
        else:
            # print("item " + str(item))
            self.itemNum -= item.qnty
            self.subtotal -= item.regularPrice * item.qnty
            self.memberSubtotal -= item.memberPrice * item.qnty

            if item.isItemTaxable():
                self.tax -= item.regularPrice * item.qnty * TAX_VALUE
                self.memberTax -= item.memberPrice * item.qnty * TAX_VALUE

            self.total = self.subtotal + self.tax
            self.memberTotal = self.memberSubtotal + self.memberTax

    # empties cart before each transaction
    def emptyCart(self):
        self.items.clear()
        self.itemNum = 0
        self.subtotal = 0.0
        self.tax = 0.0
        self.total = 0.0
        self.memberSubtotal = 0.0
        self.memberTax = 0.0
        self.memberTotal = 0.0

    # prints items in cart with totals
    def viewCart(self):
        cartHeaders = ["ITEM", "QUANTITY", "UNIT PRICE", "TOTAL"]
        headerFormat = "{:<15}" * (len(cartHeaders))
        print(headerFormat.format(*cartHeaders))

        for item in self.items:
            print("{:<15}".format(item.name) + "{:<15}".format(item.qnty), end="$")
            if self.regularCustomer:
                # print("entered")
                print("{:<14.2f}".format(item.regularPrice) + "$" + "{:<14.2f}".format(item.totalPriceRegular()))
            else:
                # print("entered")
                print("{:<14.2f}".format(item.memberPrice) + "$" + "{:<14.2f}".format(item.totalPriceMember()))