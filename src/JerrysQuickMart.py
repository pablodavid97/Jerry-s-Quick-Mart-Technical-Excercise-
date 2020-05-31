from datetime import date

# Program Constants
INVENTORY_FILE = "inventory.txt"
REGULAR_CUSTOMER = True
TAX_VALUE = 0.065

class Item:
    def __init__(self, name="", qnty=0, regularPrice=0.0, memberPrice=0.0, taxStatus="Tax-Exempt"):
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

    def __eq__(self, other):
        return self.name == other.name

    def __str__(self):
        return self.name + ": " + str(self.qnty) + ", $" + str(self.regularPrice) + ", $" + str(self.memberPrice) + ", " + self.taxStatus


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
            self.items.append(Item(name, itemInfo[0], itemInfo[1][1:], itemInfo[2][1:], itemInfo[3].replace("\n", "")))

    # updates items quantity after checkout
    def updateInventory(self, item):
        if isinstance(item, Item):
            for i in self.items:
                if item.name == i.name:
                    i.qnty = i.qnty - item.qnty


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
        self.regularCustomer = REGULAR_CUSTOMER # by default is assumed a regular customer

    # adds items if not added already (doesn't accept duplicates)
    def addItem(self, item):
        try:
            self.items.index(item)
            print("Item already in list")
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


    # removes items only if they exist (name of item should be entered with uppercases)
    def removeItem(self, name):
        n = len(self.items)
        item = Item()

        for i in range(0, n):
            if self.items[i].name == name:
                item = self.items.pop(i)
                break

        if item.name != "":
            # print("item " + str(item))
            self.itemNum -= item.qnty
            self.subtotal -= item.regularPrice * item.qnty
            self.memberSubtotal -= item.memberPrice * item.qnty

            if item.isItemTaxable():
                self.tax -= item.regularPrice * item.qnty * TAX_VALUE
                self.memberTax -= item.memberPrice * item.qnty * TAX_VALUE


            self.total = self.subtotal + self.tax
            self.memberTotal = self.memberSubtotal + self.memberTax

            return True
        else:
            return False

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

# Main object that controls the program
class JerrysQuickMart:
    def __init__(self):
        self.transactionNum = 0
        self.inventory = Inventory()
        self.cart = Cart()
        self.todayDate = date.today()
        self.menuOption = 0
        self.transactionOption = 0

    # starts the program
    def start(self):
        while True:
            self.mainMenu()
            self.menuOption = int(input("Option: "))

            if self.menuOption == 1:
                # begins new transaction
                self.newTransaction()
            elif self.menuOption == 2:
                # exits the program
                self.stop()
                break
            else:
                print("Invalid Option")

    # contains all functionalities per each transaction
    def newTransaction(self):
        # updates transaction number
        self.transactionNum += 1
        self.cart.emptyCart()
        self.cart.regularCustomer = REGULAR_CUSTOMER

        # transaction continues until user cancels it
        while True:
            try:
                self.transactionMenu()
                self.transactionOption = int(input("Option: "))

                if self.transactionOption == 1:
                    self.setCustomerType()
                elif self.transactionOption == 2:
                   self.addItemsToCart()
                elif self.transactionOption == 3:
                    self.removeItemsFromCart()
                elif self.transactionOption == 4:
                    self.viewCart()
                elif self.transactionOption == 5:
                    self.checkout()
                    break
                elif self.transactionOption == 6:
                    self.cancelTransaction()
                    break
                else:
                    print("Invalid option")
            except ValueError:
                print("Invalid option")

    def mainMenu(self):
        print("------------------------------------------------------------------------------")
        print("WELCOME TO JERRY'S QUICK MART, PLEASE SELECT ONE OF THE FOLLOWING OPTIONS")
        print("------------------------------------------------------------------------------")
        print("1. New transaction")
        print("2. Exit")

    def transactionMenu(self):
        print("------------------------------------------------------------------------------")
        print("TRANSACTION " + str(self.transactionNum) + ", PLEASE SELECT ONE OF THE FOLLOWING OPTIONS")
        print("------------------------------------------------------------------------------")
        print("1. Customer type")
        print("2. Add items to cart")
        print("3. Remove items from cart")
        print("4. View cart")
        print("5. Checkout and print receipt")
        print("6. Cancel Transaction")

    # allows to change customer type, product totals will change accordingly
    def setCustomerType(self):
        print("SET CUSTOMER TYPE")
        while True:
            response = input("Customer is a Rewards Member? (y/n): ")
            if response == "y":
                self.cart.regularCustomer = False
                break
            elif response == "n":
                self.cart.regularCustomer = True
                break

    # Adds item only if available in inventory and if it hasnt been added yet to cart
    def addItemsToCart(self):
        print("ADD ITEMS TO CART")
        print("THIS ARE THE ITEMS AVAILABLE")
        for item in self.inventory.items:
            print(item)

        info = input("Add item (item name,quantity): ").split(",")

        itemFound = False
        for item in self.inventory.items:
            if info[0] == item.name:
                if int(info[1]) <= item.qnty:
                    self.cart.addItem(
                        Item(item.name, info[1], item.regularPrice, item.memberPrice, item.taxStatus))
                    itemFound = True
                    break

        if not itemFound:
            print("Item does not exist or quantity is greater than available.")


    # removes item only if it exists
    def removeItemsFromCart(self):
        print("REMOVE ITEMS FROM CART")
        print("PLEASE SELECT ONE OF THE TWO OPTIONS BELOW")
        print("1. REMOVE ITEM")
        print("2. EMPTY CART")

        try:
            rmvOption = int(input("Option: "))
            if rmvOption == 1:
                print("THIS ARE YOUR CURRENT ITEMS IN CART")
                self.cart.viewCart()
                itemName = input("Remove item (by name): ")

                if not self.cart.removeItem(itemName):
                    print("Item does not exist please make sure you typed name correctly.")
            elif rmvOption == 2:
                self.cart.emptyCart()
            else:
                print("Invalid option")
        except ValueError:
            print("Invalid option")

    # prints items in cart with totals
    def viewCart(self):
        self.cart.viewCart()

        print("*************************************************")
        print("TOTAL NUMBER OF ITEMS: " + str(self.cart.itemNum))
        if self.cart.regularCustomer:
            print("SUB-TOTAL: $" + "{:.2f}".format(self.cart.subtotal))
            print("TAX (6.5%): $" + "{:.2f}".format(self.cart.tax))
            print("TOTAL: $" + "{:.2f}".format(self.cart.total))
            print("*************************************************")
        else:
            print("SUB-TOTAL: $" + "{:.2f}".format(self.cart.memberSubtotal))
            print("TAX (6.5%): $" + "{:.2f}".format(self.cart.memberTax))
            print("TOTAL: $" + "{:.2f}".format(self.cart.memberTotal))
            print("*************************************************")

    # allows user to checkout and print receipt
    def checkout(self):

        # allows to enter amount to pay in cash
        print("Your total is $", end=" ")
        if self.cart.regularCustomer:
            print("{:.2f}".format(self.cart.total), end=" ")
        else:
            print("{:.2f}".format(self.cart.memberTotal), end=" ")
        print(", what is the cash amount?")
        amount = float(input("Enter cash amount: "))

        print(self.todayDate.strftime("%B %d, %Y"))
        print("Transaction: " + str(self.transactionNum))

        # prints totals info depending if customer is member or not
        if self.cart.regularCustomer:
            change = amount - self.cart.total
            self.cart.viewCart()
            print("*************************************************")
            print("TOTAL NUMBER OF ITEMS SOLD: " + str(self.cart.itemNum))
            print("SUB-TOTAL: $" + "{:.2f}".format(self.cart.subtotal))
            print("TAX (6.5%): $" + "{:.2f}".format(self.cart.tax))
            print("TOTAL: $" + "{:.2f}".format(self.cart.total))
            print("CASH: $" + "{:.2f}".format(amount))
            print("CHANGE: $" + "{:.2f}".format(change))
            print("*************************************************")
        else:
            change = amount - self.cart.memberTotal
            self.cart.viewCart()
            print("*************************************************")
            print("TOTAL NUMBER OF ITEMS SOLD: " + str(self.cart.itemNum))
            print("SUB-TOTAL: $" + "{:.2f}".format(self.cart.memberSubtotal))
            print("TAX (6.5%): $" + "{:.2f}".format(self.cart.memberTax))
            print("TOTAL: $" + "{:.2f}".format(self.cart.memberTotal))
            print("CASH: $" + "{:.2f}".format(amount))
            print("CHANGE: $" + "{:.2f}".format(change))
            print("*************************************************")

            amntSaved = self.cart.total - self.cart.memberTotal
            print("YOU SAVED: $" + "{:.2f}".format(amntSaved) + "!")

        # updates items quantity after transaction
        for item in self.cart.items:
            self.inventory.updateInventory(item)

        # Updating inventory.txt
        invFile = open(INVENTORY_FILE, "w")
        for item in self.inventory.items:
            invFile.write(str(item) + "\n")

        # Printing receipt
        receiptFile = "transaction_" + "{:06d}".format(self.transactionNum) + "_" + "{:02d}".format(
            self.todayDate.month) + "{:02d}".format(self.todayDate.day) + str(self.todayDate.year) + ".txt"
        # print("Receipt file: " + receiptFile)
        receipt = open(receiptFile, "w")

        # Prints receipt differently depending if customer is member or not
        receipt.write(self.todayDate.strftime("%B %d, %Y") + "\n")
        receipt.write("Transaction: " + "{:06d}".format(self.transactionNum) + "\n")
        cartHeaders = ["ITEM", "QUANTITY", "UNIT PRICE", "TOTAL"]
        headerFormat = "{:<15}" * (len(cartHeaders))
        receipt.write(headerFormat.format(*cartHeaders) + "\n")

        if self.cart.regularCustomer:
            change = amount - self.cart.total

            for item in self.cart.items:
                receipt.write("{:<15}".format(item.name) + "{:<15}".format(item.qnty) + "$")
                receipt.write("{:<14.2f}".format(item.regularPrice) + "$" + "{:<14.2f}".format(
                    item.totalPriceRegular()) + "\n")

            receipt.write("********************************************************" + "\n")
            receipt.write("TOTAL NUMBER OF ITEMS SOLD: " + str(self.cart.itemNum) + "\n")
            receipt.write("SUB-TOTAL: $" + "{:.2f}".format(self.cart.subtotal) + "\n")
            receipt.write("TAX (6.5%): $" + "{:.2f}".format(self.cart.tax) + "\n")
            receipt.write("TOTAL: $" + "{:.2f}".format(self.cart.total) + "\n")
            receipt.write("CASH: $" + "{:.2f}".format(amount) + "\n")
            receipt.write("CHANGE: $" + "{:.2f}".format(change) + "\n")
            receipt.write("********************************************************")
        else:
            change = amount - self.cart.memberTotal
            for item in self.cart.items:
                receipt.write("{:<15}".format(item.name) + "{:<15}".format(item.qnty) + "$")
                receipt.write("{:<14.2f}".format(item.memberPrice) + "$" + "{:<14.2f}".format(
                    item.totalPriceMember()) + "\n")
            receipt.write("********************************************************" + "\n")
            receipt.write("TOTAL NUMBER OF ITEMS SOLD: " + str(self.cart.itemNum) + "\n")
            receipt.write("SUB-TOTAL: $" + "{:.2f}".format(self.cart.memberSubtotal) + "\n")
            receipt.write("TAX (6.5%): $" + "{:.2f}".format(self.cart.memberTax) + "\n")
            receipt.write("TOTAL: $" + "{:.2f}".format(self.cart.memberTotal) + "\n")
            receipt.write("CASH: $" + "{:.2f}".format(amount) + "\n")
            receipt.write("CHANGE: $" + "{:.2f}".format(change) + "\n")
            receipt.write("********************************************************" + "\n")

            amntSaved = self.cart.total - self.cart.memberTotal
            receipt.write("YOU SAVED: $" + "{:.2f}".format(amntSaved) + "!" + "\n")

    # cacels transaction
    def cancelTransaction(self):
        self.transactionNum -= 1

    # ends program
    def stop(self):
        print("Come back again soon!")

def main():
    # creates Jerry's Quick Mart Instance and begins program
    jm = JerrysQuickMart()
    jm.start()


if __name__ == "__main__":
    main()
