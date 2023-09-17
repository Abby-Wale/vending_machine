import tkinter as tk
from tkinter import ttk
import pandas as pd
from collections import Counter

items_prices = {'Slim Bar': 5, 'Far Bar': 10, 'Mar Bar': 20, 'Twin Bar': 50}
font_size = ('Arial', 24)  # Font size and family
entry_width = 20  # Width of the Entry widget in terms of number of characters
padding_x = 50 

class VendingMachine:
    def __init__(self, gui):
        self.cart = Counter()
        self.INSERTED_COIN = 0
        self.gui = gui
        self.first_coin_inserted = False
        self.update_menu()

    def reset_machine(self):
        self.cart.clear()
        self.INSERTED_COIN = 0
        self.first_coin_inserted = False
        self.update_menu()

    def update_menu(self):
        if self.first_coin_inserted:
            affordable_items = {k: v for k, v in items_prices.items() if v <= self.INSERTED_COIN}
        else:
            affordable_items = items_prices

        product_df = pd.DataFrame(list(affordable_items.items()), columns=['Products', 'Prices'])
        product_df.index += 1
        self.gui.update_menu(product_df)

    def insert_coin(self, coin):
        self.INSERTED_COIN += coin
        self.first_coin_inserted = True
        self.gui.update_balance(self.INSERTED_COIN)
        self.gui.clear_coin_entry()
        self.update_menu()

    def select_item(self, item_no):
        item_name = list(items_prices.keys())[item_no - 1]
        item_price = items_prices[item_name]
        
        if self.INSERTED_COIN >= item_price:
            self.cart[item_name] += 1
            self.INSERTED_COIN -= item_price
            self.gui.update_balance(self.INSERTED_COIN)
            self.gui.update_cart(self.cart)
            self.update_menu()
        else:
            self.gui.notify_insufficient_funds()

class VendingMachineGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Vending Machine")
        self.master.geometry("450x600")  # Set the size of the window

 # Horizontal padding for widgets

        self.menu_label = tk.Label(self.master, text="Menu", font=font_size)
        self.menu_label.grid(row=0, column=0, padx=padding_x)

        self.balance_label = tk.Label(self.master, text="Balance: 0", font=font_size)
        self.balance_label.grid(row=1, column=0, padx=padding_x)

        self.vm = VendingMachine(self)

        self.insert_coin_button = tk.Button(self.master, text="Insert Coin", command=self.insert_coin, font=font_size)
        self.insert_coin_button.grid(row=2, column=0, padx=padding_x)

        self.coin_entry = ttk.Entry(self.master, width=entry_width, font=font_size)
        self.coin_entry.grid(row=3, column=0, padx=padding_x)

        self.select_button = tk.Button(self.master, text="Select Item", command=self.select_item, font=font_size)
        self.select_button.grid(row=4, column=0, padx=padding_x)

        self.item_no_entry = ttk.Entry(self.master, width=entry_width, font=font_size)
        self.item_no_entry.grid(row=5, column=0, padx=padding_x)

        self.done_button = tk.Button(self.master, text="Done", command=self.done, font=font_size)
        self.done_button.grid(row=6, column=0, padx=padding_x)

        self.cart_label = tk.Label(self.master, text="Cart", font=font_size)
        self.cart_label.grid(row=7, column=0, padx=padding_x)


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
        self.reset_button()

    def reset_button(self):
        self.reset_button = tk.Button(self.master, text="Reset", command=self.reset_machine, font=font_size)
        self.reset_button.grid(row=8, column=0, padx=padding_x)


    def reset_machine(self):
        self.vm.reset_machine()
        self.update_balance(0)
        self.cart_label['text'] = "Cart"
        self.insert_coin_button['state'] = tk.NORMAL
        self.select_button['state'] = tk.NORMAL
        self.reset_button.destroy()

    def show_receipt(self):
        receipt = "Receipt\n" + "-" * 20 + "\n"
        total_cost = 0
        for item, qty in self.vm.cart.items():
            cost = items_prices[item] * qty
            total_cost += cost
            receipt += f"{item} x{qty} = {cost}p\n"
        receipt += "-" * 20
        receipt += f"\nTotal: {total_cost}p\nChange: {self.vm.INSERTED_COIN}p"
        self.cart_label['text'] = receipt


    

if __name__ == "__main__":
    root = tk.Tk()
    app = VendingMachineGUI(root)
    root.mainloop()

