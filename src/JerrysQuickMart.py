from datetime import date

inventoryFile = "inventory.txt"
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
        file = open(inventoryFile, "r")

        for line in file:
            # print(line)
            item = line.split(": ")
            name = item[0]
            itemInfo = item[1].split(", ")
            # print("regularPrice: " + str(itemInfo[1][1:]))
            # print("memberPrice: " + str(itemInfo[2][1:]))
            self.items.append(Item(name, itemInfo[0], itemInfo[1][1:], itemInfo[2][1:], itemInfo[3].replace("\n", "")))

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
        self.memberSubtotal = 0.0
        self.memberTax = 0.0
        self.memberTotal = 0.0
        self.regularCustomer = regularCustomer

    def addItem(self, item):
        self.items.append(item)
        self.itemNum += item.qnty

        self.subtotal += item.regularPrice * item.qnty

        if item.taxStatus == "Taxable":
            self.tax += item.regularPrice * item.qnty * taxValue

        self.total = self.subtotal + self.tax

        if not self.regularCustomer:
            self.memberSubtotal += item.memberPrice * item.qnty

            if item.taxStatus == "Taxable":
                self.memberTax += item.memberPrice * item.qnty * taxValue

            self.memberTotal = self.memberSubtotal + self.memberTax

    def removeItem(self, name):
        n = len(self.items)
        item = None

        for i in range(0, n):
            if self.items[i].name == name:
                item = self.items.pop(i)

        if item != None:
            # print("item " + str(item))
            self.itemNum -= item.qnty
            self.subtotal -= item.regularPrice * item.qnty
            self.memberSubtotal -= item.memberPrice * item.qnty

            if item.taxStatus == "Taxable":
                self.tax -= item.regularPrice * item.qnty * taxValue
                self.memberTax -= item.memberPrice * item.qnty * taxValue


            self.total = self.subtotal + self.tax
            self.memberTotal = self.memberSubtotal + self.memberTax

    def emptyCart(self):
        self.items.clear()
        self.itemNum = 0
        self.subtotal = 0.0
        self.tax = 0.0
        self.total = 0.0
        self.memberSubtotal = 0.0
        self.memberTax = 0.0
        self.memberTotal = 0.0


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
                        cart.regularCustomer = True
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

                print("Your total is $", end=" ")
                if cart.regularCustomer:
                    print("{:.2f}".format(cart.total), end=" ")
                else:
                    print("{:.2f}".format(cart.memberTotal), end=" ")
                print(", what is the cash amount?")
                amount = float(input("Enter cash amount: "))

                if cart.regularCustomer:
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
                else:
                    change = amount - cart.memberTotal
                    print(todayDate.isoformat())
                    print("Transaction: " + str(transactionNum))
                    cart.viewCart()
                    print("*******************************")
                    print("TOTAL NUMBER OF ITEMS SOLD: " + str(cart.itemNum))
                    print("SUB-TOTAL: $" + "{:.2f}".format(cart.memberSubtotal))
                    print("TAX (6.5%): $" + "{:.2f}".format(cart.memberTax))
                    print("TOTAL: $" + "{:.2f}".format(cart.memberTotal))
                    print("CASH: $" + "{:.2f}".format(amount))
                    print("CHANGE: $" + "{:.2f}".format(change))
                    print("*******************************")

                    amntSaved = cart.total - cart.memberTotal
                    print("YOU SAVED: $" + "{:.2f}".format(amntSaved) + "!")

                for item in cart.items:
                    inventory.updateInventory(item)

                # Updating inventory.txt
                invFile = open(inventoryFile, "w")
                for item in inventory.items:
                    invFile.write(str(item) + "\n")

                # Printing receipt
                receiptFile = "transaction_" + "{:06d}".format(transactionNum) + "_" + "{:02d}".format(todayDate.month) + "{:02d}".format(todayDate.day) + str(todayDate.year) + ".txt"
                # print("Receipt file: " + receiptFile)

                receipt = open(receiptFile, "w")

                if cart.regularCustomer:
                    change = amount - cart.total
                    receipt.write(todayDate.isoformat() + "\n")
                    receipt.write("Transaction: " + "{:06d}".format(transactionNum) + "\n")

                    receipt.write("ITEM\tQUANTITY\tUNIT PRICE\tTOTAL" + "\n")
                    for item in cart.items:
                        receipt.write(item.name + "\t" + str(item.qnty) + "\t\t\t$")
                        receipt.write("{:.2f}".format(item.regularPrice) + "\t\t$" + "{:.2f}".format(
                            item.totalPriceRegular()) + "\n")

                    receipt.write("*******************************" + "\n")
                    receipt.write("TOTAL NUMBER OF ITEMS SOLD: " + str(cart.itemNum) + "\n")
                    receipt.write("SUB-TOTAL: $" + "{:.2f}".format(cart.subtotal) + "\n")
                    receipt.write("TAX (6.5%): $" + "{:.2f}".format(cart.tax) + "\n")
                    receipt.write("TOTAL: $" + "{:.2f}".format(cart.total) + "\n")
                    receipt.write("CASH: $" + "{:.2f}".format(amount) + "\n")
                    receipt.write("CHANGE: $" + "{:.2f}".format(change) + "\n")
                    receipt.write("*******************************")
                else:
                    change = amount - cart.memberTotal
                    receipt.write(todayDate.isoformat() + "\n")
                    receipt.write("Transaction: " + "{:06d}".format(transactionNum) + "\n")

                    receipt.write("ITEM\tQUANTITY\tUNIT PRICE\tTOTAL" + "\n")
                    for item in cart.items:
                        receipt.write(item.name + "\t" + str(item.qnty) + "\t\t\t$")
                        receipt.write("{:.2f}".format(item.memberPrice) + "\t\t$" + "{:.2f}".format(
                            item.totalPriceMember()) + "\n")
                    receipt.write("*******************************" + "\n")
                    receipt.write("TOTAL NUMBER OF ITEMS SOLD: " + str(cart.itemNum) + "\n")
                    receipt.write("SUB-TOTAL: $" + "{:.2f}".format(cart.memberSubtotal) + "\n")
                    receipt.write("TAX (6.5%): $" + "{:.2f}".format(cart.memberTax) + "\n")
                    receipt.write("TOTAL: $" + "{:.2f}".format(cart.memberTotal) + "\n")
                    receipt.write("CASH: $" + "{:.2f}".format(amount) + "\n")
                    receipt.write("CHANGE: $" + "{:.2f}".format(change) + "\n")
                    receipt.write("*******************************" + "\n")

                    amntSaved = cart.total - cart.memberTotal
                    receipt.write("YOU SAVED: $" + "{:.2f}".format(amntSaved) + "!" + "\n")

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
