# Jerry-s-Quick-Mart-Technical-Excercise-
Jerry’s Quick Mart in Orlando, FL is having its grand opening in 3 days. His previously hired software team lost all their files, and Jerry needs a solution for his grand opening.

# Solution
For this exercise and in order to comply with Object Oriented Programming requirements I decided to create 4 main classes that are shown below:


## Main classes
1. Item: Item is an object that holds information for the items in the market, that is the name of the item, the quantity in stock, the regular price, the price for members, and if the item is taxable or not. It is the simplest unit of the program.
2. Inventory: Inventory is a list of Items, and is the object representation of the input file that is used for this program 
3. Cart: Cart is also a list of Items and it represents the cart that belongs to a specific customer making a transaction. This class holds additional information that is used to print the receipt and show the information related to the user’s purchase. 
4. JerrysQuickMart: This is the main class that is composed by the rest of the classes and that controls the sequence or flow of the program. It contains eleven methods that are used to comply with necessary functionalities.

## Brief description of the program

To start the program the user must run it from the jerrysquickmart.py file which contains the class and the main method that runs the program. The method that starts everything is called start() and the first thing it will do is to load the inventory file into the inventory object defined. 

After this the program will display the main menu and run continuously until told otherwise by the user. The main menu has two options: begin a new transaction or end program. If the user decides to create a new transaction it must select this option. After this the program will set track of the transactions and will show the transaction menu that will allow the user to perform the basic functionalities: set the customer type, add items to cart, remove items to cart with empty cart option, view cart, proceed to checkout and cancel transaction. 

Each one of the options has a data validation handled by exceptions if necessary in order to provide feedback to the user. If the user wants to cancel the transaction he/she must choose this option and the program will return to the main menu. Otherwise, if the user wants to proceed to checkout the program will ask for the amount in cash, and it will print the receipt and update the stock. 


## Assumptions made 
The customer is set to regular by default but it can be changed within the program and the final values will be changed accordingly. 
The tax value is 6.5% but it can be changed if necessary.
The transaction number is not stored anywhere, and so it will start from 1. For this is assumed that the program will run continuously each day and therefore each transaction will be tracked. 
Inventory items are shown before adding and removing an item.


## How to run the code
All the main classes are located in the src folder as well as the inventory. To run the program use the following command

python3 jerrysquickmart.py or python jerrysquickmart.py

Also the project can be included within any IDE, for this case Pycharm Community was used. 

## How to run unit testings

There are four unit tests that are part of the program and are also located in the src folder. To run each test you must run the following command:

python -m unittest test_name

For example 

python -m unittest test_cart.py
