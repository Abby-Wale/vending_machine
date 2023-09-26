Overview

The Vending Machine Simulator is a Python application that simulates the functionality of a real-world vending machine. 
The application is built using the Tkinter library for the graphical user interface (GUI) and Pandas for data manipulation. 
It allows users to insert coins, select items, and complete transactions, all while updating the available items and balance in real-time.

Features
- Dynamic Menu: The menu updates based on the coins inserted, showing only the items that can be afforded.
- Cart Management: Users can add items to their cart and view it before completing the transaction.
- Coin Insertion: Users can insert coins to increase their balance.
- Transaction Completion: A receipt is generated upon transaction completion, showing the items purchased and the change returned.
- Reset Functionality: The machine can be reset to its initial state.

Installation
To run the Vending Machine Simulator, you'll need Python 3.x installed on your machine. 
You'll also need to install Pandas.


Usage
1. Clone the repository to your local machine.
2. Navigate to the directory containing the script.
3. Run the script using Python.   `python vending_machine_simulator.py`

Code Structure
- `VendingMachine`: The core class that handles the logic of the vending machine.
  - `__init__`: Initializes the vending machine.
  - `reset_machine`: Resets the machine to its initial state.
  - `update_menu`: Updates the menu based on the inserted coins.
  - `insert_coin`: Handles coin insertion.
  - `select_item`: Handles item selection.

- `VendingMachineGUI`: The class responsible for the GUI.
  - `__init__`: Initializes the GUI.
  - `update_menu`: Updates the menu display.
  - `insert_coin`: Inserts coin into the machine.
  - `clear_coin_entry`: Clears the coin entry field.
  - `update_balance`: Updates the displayed balance.
  - `select_item`: Selects an item based on its number.
  - `update_cart`: Updates the cart display.
  - `notify_insufficient_funds`: Displays a message for insufficient funds.
  - `done`: Completes the transaction and shows the receipt.
  - `reset_machine`: Resets the machine and the GUI.

Dependencies
- Tkinter
- Pandas
- Collections (Counter)

Contributing
Feel free to fork the repository and submit pull requests. For major changes, please open an issue first to discuss what you'd like to change.

License
This project is licensed under the MIT License. See the `LICENSE` file for details.
