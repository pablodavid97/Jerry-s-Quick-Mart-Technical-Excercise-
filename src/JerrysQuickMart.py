from datetime import date

fileName = "inventory.txt"
regularCustomer = False
taxValue = 0.065


class Item:
    def __init__(self, name, qnty, regularPrice, memberPrice, taxStatus):
        self.name = name
        self.qnty = int(qnty)
        self.regularPrice = float(regularPrice)
        self.memberPrice = float(memberPrice)
        self.taxStatus = taxStatus

    def isItemTaxable(self):
        if self.taxStatus == "Taxable":
            return True
        else:
            return False

    def totalPriceRegular(self):
        return self.regularPrice * self.qnty

    def totalPriceMember(self):
        return self.memberPrice * self.qnty

    def __str__(self):
        return self.name + ": " + str(self.qnty) + ", $" + str(self.regularPrice) + ", $" + str(self.memberPrice) + ", " + self.taxStatus


class Inventory:
    def __init__(self):
        self.items = []
        self.loadInventory()

    def loadInventory(self):
        file = open(fileName, "r")

        for line in file:
            print(line)
            item = line.split(": ")
            name = item[0]
            itemInfo = item[1].split(", ")
            # print("regularPrice: " + str(itemInfo[1][1:]))
            # print("memberPrice: " + str(itemInfo[2][1:]))
            self.items.append(Item(name, itemInfo[0], itemInfo[1][1:], itemInfo[2][1:], itemInfo[3][:-1]))

    def updateInventory(self, item):
        if isinstance(item, Item):
            for i in self.items:
                if item.name == i.name:
                    i.qnty = str(int(i.qnty) - int(item.qnty))


class Cart:
    def __init__(self):
        self.items = []
        self.itemNum = 0
        self.subtotal = 0.0
        self.tax = 0.0
        self.total = 0.0
        self.regularCustomer = regularCustomer

    def addItem(self, item):
        self.items.append(item)
        self.itemNum += item.qnty

        if self.regularCustomer:
            self.subtotal += item.regularPrice * item.qnty

            if item.taxStatus == "Taxable":
                self.tax += item.regularPrice * item.qnty * taxValue
        else:
            self.subtotal += item.memberPrice * item.qnty

            if item.taxStatus == "Taxable":
                self.tax += item.memberPrice * item.qnty * taxValue

        self.total = self.subtotal + self.tax

    def removeItem(self, name):
        self.items = [item for item in self.items if not item.name == name]
        self.itemNum -= 1

    def emptyCart(self):
        self.items.clear()
        self.itemNum = 0
        self.tax = 0.0
        self.subtotal = 0.0
        self.total = 0.0

    def viewCart(self):
        print("ITEM\tQUANTITY\tUNIT PRICE\tTOTAL")
        for item in self.items:
            print(item.name + "\t" + str(item.qnty), end="\t\t\t$")
            if self.regularCustomer:
                # print("entered")
                print("{:.2f}".format(item.regularPrice) + "\t\t$" + "{:.2f}".format(item.totalPriceRegular()))
            else:
                # print("entered")
                print("{:.2f}".format(item.memberPrice) + "\t\t$" + "{:.2f}".format(item.totalPriceMember()))


def main():
    transactionNum = 1
    inventory = Inventory()
    cart = Cart()
    todayDate = date.today()

    while True:
        # print(regularCustomer)
        print("------------------------------------------------------------------------------")
        print("WELCOME TO JERRY'S QUICK MART, PLEASE SELECT ONE OF THE FOLLOWING OPTIONS")
        print("------------------------------------------------------------------------------")
        print("1. Customer type")
        print("2. Add items to cart")
        print("3. Remove items from cart")
        print("4. View cart")
        print("5. Checkout and print receipt")
        print("6. Cancel Transaction")

        try:
            option = int(input("Option: "))

            if option == 1:
                print("SET CUSTOMER TYPE")
                while True:
                    response = input("Customer is a Rewards Member? (y/n): ")
                    if response == "y":
                        cart.regularCustomer = False
                        break
                    elif response == "n":
                        break
            elif option == 2:
                print("ADD ITEMS TO CART")
                print("THIS ARE THE ITEMS AVAILABLE")
                for item in inventory.items:
                    print(item)

                info = input("Add item (item name,quantity): ").split(",")

                itemFound = False
                for item in inventory.items:
                    if info[0] == item.name:
                        if int(info[1]) <= item.qnty:
                            cart.addItem(Item(item.name, info[1], item.regularPrice, item.memberPrice, item.taxStatus))
                            itemFound = True
                            break

                if not itemFound:
                    print("Item does not exist or quantity is greater than available.")
            elif option == 3:
                print("REMOVE ITEMS FROM CART")
                print("PLEASE SELECT ONE OF THE TWO OPTIONS BELOW")
                print("1. REMOVE ITEM")
                print("2. EMPTY CART")

                try:
                    rmvOption = int(input("Option: "))
                    if rmvOption == 1:
                        print("THIS ARE YOUR CURRENT ITEMS IN CART")
                        cart.viewCart()
                        itemName = input("Remove item (by name): ")

                        cart.removeItem(itemName)
                    elif rmvOption == 2:
                        cart.emptyCart()
                    else:
                        print("Invalid option")
                except ValueError:
                    print("Invalid option")
            elif option == 4:
                cart.viewCart()
            elif option == 5:
                print("Your total is $" + str(cart.total) + ", what is the cash amount?")
                amount = float(input("Enter cash amount: "))
                change = amount - cart.total

                print(todayDate.isoformat())
                print("Transaction: " + str(transactionNum))
                cart.viewCart()
                print("*******************************")
                print("TOTAL NUMBER OF ITEMS SOLD: " + str(cart.itemNum))
                print("SUB-TOTAL: $" + "{:.2f}".format(cart.subtotal))
                print("TAX (6.5%): $" + "{:.2f}".format(cart.tax))
                print("TOTAL: $" + "{:.2f}".format(cart.total))
                print("CASH: $" + "{:.2f}".format(amount))
                print("CHANGE: $" + "{:.2f}".format(change))
                print("*******************************")

                if not regularCustomer:
                    print("YOU SAVED: $" + "!")

                for item in cart.items:
                    inventory.updateInventory(item)

                for item in inventory.items:
                    print(item)
                break
            elif option == 6:
                transactionNum -= 1
                break
            else:
                print("Invalid option")
        except ValueError:
            print("Invalid option")

    print("Come back again soon!")


if __name__ == "__main__":
    main()
