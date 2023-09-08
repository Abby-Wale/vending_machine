import tkinter as tk
from tkinter import ttk
import pandas as pd
from collections import Counter

items_prices = {'Slim Bar': 5, 'Far Bar': 10, 'Mar Bar': 20, 'Twin Bar': 50}

class VendingMachine:
    def __init__(self, gui):
        self.cart = Counter()
        self.INSERTED_COIN = 0
        self.gui = gui
        self.update_menu()

    def update_menu(self):
        product_df = pd.DataFrame(list(items_prices.items()), columns=['Products', 'Prices'])
        product_df.index += 1  
        self.gui.update_menu(product_df)

    def insert_coin(self, coin):
        self.INSERTED_COIN += coin
        self.gui.update_balance(self.INSERTED_COIN)
        self.gui.clear_coin_entry()

    def select_item(self, item_no):
        item_name = list(items_prices.keys())[item_no - 1]
        item_price = items_prices[item_name]
        
        if self.INSERTED_COIN >= item_price:
            self.cart[item_name] += 1
            self.INSERTED_COIN -= item_price
            self.gui.update_balance(self.INSERTED_COIN)
            self.gui.update_cart(self.cart)
        else:
            self.gui.notify_insufficient_funds()

class VendingMachineGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Vending Machine")
        
        self.menu_label = ttk.Label(self.master, text="Menu")
        self.menu_label.grid(row=0, column=0, columnspan=2)
        
        self.balance_label = ttk.Label(self.master, text="Balance: 0")
        self.balance_label.grid(row=1, column=1)
        
        self.vm = VendingMachine(self)
        
        self.coin_entry = ttk.Entry(self.master)
        self.coin_entry.grid(row=2, column=1)
        
        self.insert_coin_button = ttk.Button(self.master, text="Insert Coin", command=self.insert_coin)
        self.insert_coin_button.grid(row=2, column=0)
        
        self.item_no_entry = ttk.Entry(self.master)
        self.item_no_entry.grid(row=3, column=1)
        
        self.select_button = ttk.Button(self.master, text="Select Item", command=self.select_item)
        self.select_button.grid(row=3, column=0)
        
        self.done_button = ttk.Button(self.master, text="Done", command=self.done)
        self.done_button.grid(row=4, column=0)
        
        self.cart_label = ttk.Label(self.master, text="Cart")
        self.cart_label.grid(row=5, column=0, columnspan=2)

    def update_menu(self, product_df):
        self.menu_label['text'] = str(product_df)

    def insert_coin(self):
        coin = int(self.coin_entry.get())
        self.vm.insert_coin(coin)

    def clear_coin_entry(self):
        self.coin_entry.delete(0, tk.END)

    def update_balance(self, balance):
        self.balance_label['text'] = f"Balance: {balance}"

    def select_item(self):
        item_no = int(self.item_no_entry.get())
        self.vm.select_item(item_no)
        self.item_no_entry.delete(0, tk.END)  

    def update_cart(self, cart):
        cart_df = pd.DataFrame(list(cart.items()), columns=['Products', 'Qty'])
        cart_df.index += 1 
        self.cart_label['text'] = str(cart_df)

    def notify_insufficient_funds(self):
        self.cart_label['text'] = "Insufficient funds. Transaction terminated."

    def done(self):
        self.insert_coin_button['state'] = tk.DISABLED
        self.select_button['state'] = tk.DISABLED
        self.show_receipt()

    def show_receipt(self):
        receipt = "Receipt\n" + "-" * 20 + "\n"
        for item, qty in self.vm.cart.items():
            receipt += f"{item}: {qty}\n"
        receipt += "-" * 20
        receipt += f"\nTotal: {self.vm.INSERTED_COIN}"
        self.cart_label['text'] = receipt

if __name__ == "__main__":
    root = tk.Tk()
    app = VendingMachineGUI(root)
    root.mainloop()
