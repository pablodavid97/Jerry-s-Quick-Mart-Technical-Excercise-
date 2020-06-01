from datetime import date
from cart import Cart
from inventory import Inventory

# Program Constants
INVENTORY_FILE = "inventory.txt"
REGULAR_CUSTOMER = True
TAX_VALUE = 0.065

# Main object that controls the program
class JerrysQuickMart:
    def __init__(self):
        self.transactionNum = 0
        self.inventory = Inventory()
        self.cart = Cart()
        self.todayDate = date.today()
        self._customerOption = ""
        self._menuOption = 0
        self._transactionOption = 0
        self._addInput = []
        self._cashAmount = 0.0
        self._rmvOption = 0

    @property
    def customerOption(self):
        return self._customerOption

    @customerOption.setter
    def customerOption(self, option):
        if not isinstance(option, str):
            raise TypeError("Response should be a letter")

        if option != "y" and option != "n":
            raise ValueError("Response should be either 'y' or 'n'!")

        self._customerOption = option

    @property
    def menuOption(self):
        return self._menuOption

    @menuOption.setter
    def menuOption(self, option):

        if not isinstance(option, int):
            raise TypeError("Option should be a number!")

        if option != 1 and option != 2:
            raise ValueError("Option should be either 1 or 2!")

        self._menuOption = option

    @property
    def transactionOption(self):
        return self._transactionOption

    @transactionOption.setter
    def transactionOption(self, option):
        if not isinstance(option, int):
            raise TypeError("Option should be a number!")

        if option < 1 or option > 6:
            raise ValueError("Option should be between 1 and 6!")

        self._transactionOption = option

    @property
    def addInput(self):
        return self._addInput

    @addInput.setter
    def addInput(self, input):
        if len(input) != 2:
            raise ValueError("Invalid format! Required 2 arguments item name and quantity")

        if not isinstance(input[0], str):
            raise TypeError("Name of item should be a string!")

        if not isinstance(input[1], int) or input[1] < 0:
            raise TypeError("Quantity should be a positive integer!")

        self._addInput = input

    @property
    def rmvOption(self):
        return self._rmvOption

    @rmvOption.setter
    def rmvOption(self, option):
        if not isinstance(option, int):
            raise TypeError("Option should be a number!")

        if option != 1 and option != 2:
            raise ValueError("Option should be either 1 or 2!")

        self._rmvOption = option

    @property
    def cashAmount(self):
        return self._cashAmount

    @cashAmount.setter
    def cashAmount(self, amount):
        if not isinstance(amount, float):
            raise TypeError("Cash amount should be a decimal number!")

        self._cashAmount = amount

    # starts the program
    def start(self):
        while True:
            try:
                self.mainMenu()
                self.menuOption = int(input("Option: "))

                if self.menuOption == 1:
                    # begins new transaction
                    self.newTransaction()
                elif self.menuOption == 2:
                    # exits the program
                    self.stop()
                    break
            except TypeError as te:
                print(te)
            except ValueError as ve:
                print(ve)

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
            except TypeError as te:
                print(te)
            except ValueError as ve:
                print(ve)

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
            self.customerOption = input("Customer is a Rewards Member? (y/n): ")
            if self.customerOption == "y":
                self.cart.regularCustomer = False
                break
            elif self.customerOption == "n":
                self.cart.regularCustomer = True
                break

    # Adds item only if available in inventory and if it hasnt been added yet to cart
    def addItemsToCart(self):
        print("ADD ITEMS TO CART")
        print("THIS ARE THE ITEMS AVAILABLE")
        for item in self.inventory.items:
            print(item)

        info = input("Add item (item name,quantity): ").split(",")
        if(len(info) > 1):
            info[1] = int(info[1])
        self.addInput = info

        itemFound = False
        for item in self.inventory.items:
            if self.addInput[0] == item.name:
                if self.addInput[1] <= item.qnty:
                    self.cart.addItem(
                        item(item.name, self.addInput[1], item.regularPrice, item.memberPrice, item.taxStatus))
                    itemFound = True
                    break
                else:
                    raise ValueError("Quantity is greater than available")

        if not itemFound:
           raise ValueError("Item not found or does not exist, make you sure item name is typed correctly!")


    # removes item only if it exists
    def removeItemsFromCart(self):
        print("REMOVE ITEMS FROM CART")
        print("PLEASE SELECT ONE OF THE TWO OPTIONS BELOW")
        print("1. REMOVE ITEM")
        print("2. EMPTY CART")

        self.rmvOption = int(input("Option: "))
        if self.rmvOption == 1:
            print("THIS ARE YOUR CURRENT ITEMS IN CART")
            self.cart.viewCart()
            itemName = input("Remove item (by name): ")

            self.cart.removeItem(itemName)

        elif self.rmvOption == 2:
            self.cart.emptyCart()

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
        self.cashAmount = float(input("Enter cash amount: "))

        print(self.todayDate.strftime("%B %d, %Y"))
        print("Transaction: " + str(self.transactionNum))

        # prints totals info depending if customer is member or not
        if self.cart.regularCustomer:
            change = self.cashAmount - self.cart.total
            self.cart.viewCart()
            print("*************************************************")
            print("TOTAL NUMBER OF ITEMS SOLD: " + str(self.cart.itemNum))
            print("SUB-TOTAL: $" + "{:.2f}".format(self.cart.subtotal))
            print("TAX (6.5%): $" + "{:.2f}".format(self.cart.tax))
            print("TOTAL: $" + "{:.2f}".format(self.cart.total))
            print("CASH: $" + "{:.2f}".format(self.cashAmount))
            print("CHANGE: $" + "{:.2f}".format(change))
            print("*************************************************")
        else:
            change = self.cashAmount - self.cart.memberTotal
            self.cart.viewCart()
            print("*************************************************")
            print("TOTAL NUMBER OF ITEMS SOLD: " + str(self.cart.itemNum))
            print("SUB-TOTAL: $" + "{:.2f}".format(self.cart.memberSubtotal))
            print("TAX (6.5%): $" + "{:.2f}".format(self.cart.memberTax))
            print("TOTAL: $" + "{:.2f}".format(self.cart.memberTotal))
            print("CASH: $" + "{:.2f}".format(self.cashAmount))
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
            change = self.cashAmount - self.cart.total

            for item in self.cart.items:
                receipt.write("{:<15}".format(item.name) + "{:<15}".format(item.qnty) + "$")
                receipt.write("{:<14.2f}".format(item.regularPrice) + "$" + "{:<14.2f}".format(
                    item.totalPriceRegular()) + "\n")

            receipt.write("********************************************************" + "\n")
            receipt.write("TOTAL NUMBER OF ITEMS SOLD: " + str(self.cart.itemNum) + "\n")
            receipt.write("SUB-TOTAL: $" + "{:.2f}".format(self.cart.subtotal) + "\n")
            receipt.write("TAX (6.5%): $" + "{:.2f}".format(self.cart.tax) + "\n")
            receipt.write("TOTAL: $" + "{:.2f}".format(self.cart.total) + "\n")
            receipt.write("CASH: $" + "{:.2f}".format(self.cashAmount) + "\n")
            receipt.write("CHANGE: $" + "{:.2f}".format(change) + "\n")
            receipt.write("********************************************************")
        else:
            change = self.cashAmount - self.cart.memberTotal
            for item in self.cart.items:
                receipt.write("{:<15}".format(item.name) + "{:<15}".format(item.qnty) + "$")
                receipt.write("{:<14.2f}".format(item.memberPrice) + "$" + "{:<14.2f}".format(
                    item.totalPriceMember()) + "\n")
            receipt.write("********************************************************" + "\n")
            receipt.write("TOTAL NUMBER OF ITEMS SOLD: " + str(self.cart.itemNum) + "\n")
            receipt.write("SUB-TOTAL: $" + "{:.2f}".format(self.cart.memberSubtotal) + "\n")
            receipt.write("TAX (6.5%): $" + "{:.2f}".format(self.cart.memberTax) + "\n")
            receipt.write("TOTAL: $" + "{:.2f}".format(self.cart.memberTotal) + "\n")
            receipt.write("CASH: $" + "{:.2f}".format(self.cashAmount) + "\n")
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
