class Item:
    def __init__(self, name="", qnty=0, regularPrice=0.0, memberPrice=0.0, taxStatus="Tax-Exempt"):
        self.name = name
        self._qnty = qnty
        self._regularPrice = regularPrice
        self._memberPrice = memberPrice
        self.taxStatus = taxStatus

    @property
    def qnty(self):
        return self._qnty

    @qnty.setter
    def qnty(self, number):
        if not isinstance(number, int) or number < 0:
            raise TypeError("Item quantity should be a positive integer number!")

        self._qnty = number

    @property
    def regularPrice(self):
        return self._regularPrice

    @regularPrice.setter
    def regularPrice(self, price):
        if not isinstance(price, float) or price < 0.0:
            raise TypeError("Price should be a positive decimal number!")

        self._regularPrice = price

    @property
    def memberPrice(self):
        return self._memberPrice

    @memberPrice.setter
    def memberPrice(self, price):
        if not isinstance(price, float) or price < 0.0:
            raise TypeError("Price should be a positive decimal number!")

        self._memberPrice = price

    def isItemTaxable(self):
        if self.taxStatus == "Taxable":
            return True
        else:
            return False

    def totalPriceRegular(self):
        return self.regularPrice * self.qnty

    def totalPriceMember(self):
        return self.memberPrice * self.qnty

    def __eq__(self, other):
        return self.name == other.name

    def __str__(self):
        return self.name + ": " + str(self.qnty) + ", $" + str(self.regularPrice) + ", $" + str(self.memberPrice) + ", " + self.taxStatus