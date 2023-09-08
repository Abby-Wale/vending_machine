import numpy as np
from datetime import date
import pandas as pd

""" the user sees the menu as the machine initializes.
    thereafter, the inserted coin determines what is
    displayed on menu.
    at every stage of transaction, the machine displays
    only what the user change can afford.
    I decided to use a class because it gives a better control 
    as much as a finite state machine would do """

items_prices = {
    'Slim Bar': 5,
    'Far Bar': 10,
    'Mar Bar': 20,
    'Twin Bar': 50
}


class VendingMachine:
    cart = []
    INSERTED_COIN = 0
    new_balance = 0

    def __init__(self):
        """
        the constructor displays the menu when the vending machine
        is initialized
        """
        product_df = pd.DataFrame(list(items_prices.items()), columns=['Products', 'Prices'])
        product_df.index += 1
        print('*********MENU*********')
        print(f'{product_df}\n')

    @staticmethod
    def insert_coin():
        """this static method prompts the user to insert a coin"""
        coins = [5, 10, 20, 50]
        while True:
            try:
                print('coins(pence) accepted are 5, 10, 20 & 50')
                coin = int(input('Insert coin here >>>  '))
                if coin in coins:
                    print(f'You have {coin}p in your account.')
                    VendingMachine.INSERTED_COIN += coin
                    # new_balance is initialized to the value of inserted coin.
                    # INSERTED_COIN is a constant while new_balance decreases after each purchase.
                    VendingMachine.new_balance += coin
                    break
                else:
                    raise ValueError
            except ValueError:
                print('Oops! that was an invalid coin')

    def menu_list(self):
        """ this method removes any item that the cost is above the user's
            inserted coin or change from the menu list """
        for key in list(items_prices.keys()):
            if items_prices[key] > VendingMachine.new_balance:
                del items_prices[key]
        self.new_dic = items_prices
        # pandas is used here to display my menu for a better outlook
        product_df1 = pd.DataFrame(list(self.new_dic.items()), columns=['Products', 'Prices'])
        product_df1.index += 1
        print(product_df1)
        print()

    @staticmethod
    def numbers_():
        """
            this method returns the number/numbers that helps
            to control display menu, base on the user's
            inserted coin/change
        """
        numbers = []
        if 0 < VendingMachine.new_balance < 10:
            numbers += [1]
        elif 0 < VendingMachine.new_balance < 20:
            numbers += [1, 2]
        elif 0 < VendingMachine.new_balance < 35:
            numbers += [1, 2, 3]
        elif VendingMachine.new_balance > 0 and VendingMachine.INSERTED_COIN > 45:
            numbers += [1, 2, 3, 4]
        return numbers

    def select_choc(self):
        """
        the method request the user to input
        his/her choice item's serial number
        """
        while True:
            try:
                self.item_no = int(input('\nPlease, input item number >>>  '))
                if self.item_no in VendingMachine.numbers_():
                    self.idx = self.item_no - 1
                    self.each_cost = list(self.new_dic.values())[self.idx]
                    return self.each_cost
                else:
                    print('Oops! that was out of range')
            except ValueError:
                print("Oops! That was a wrong value")

    def quantity(self):
        """this method prompts the user to input item quantity """
        while True:
            try:
                self.item_qty = int(input('Please, select item quantity >>> '))
                self.qty_cost = self.item_qty * self.each_cost
                if self.qty_cost <= VendingMachine.new_balance:
                    VendingMachine.new_balance -= self.qty_cost
                    ret = list(items_prices.keys())[self.idx]
                    qty_of_items = self.item_qty * [ret]
                    VendingMachine.cart.append(qty_of_items)
                    print(f'You have added {self.item_qty} \'{ret}\' to your cart')
                    break
                else:
                    print(f'Your selection cost {self.qty_cost}p')
                    print(f'You have {VendingMachine.new_balance}p in your account')
                    print('Try again')
            except ValueError:
                print("invalid input")

    @staticmethod
    def date():
        """
        this method is used to print transaction
        date on the user's receipt
        """
        today = date.today()
        print(f'   {today.strftime("%b-%d-%Y")}')


def vend():
    """
    this function runs the vending machine
    """
    print('University of Suffolk Vending Machine')
    vm = VendingMachine()
    vm.insert_coin()
    keep_buying = True
    to_cancel = ['y', 'n']
    while True:
        try:
            # the cancel variable gives the user an option to take back his/her coin if
            # he/she decides against the transaction
            cancel = input('\nPress "y" to cancel transaction\nPress "n" to continue >>> ').lower()
            if cancel in to_cancel:
                if cancel == 'y':
                    print(f'{VendingMachine.INSERTED_COIN}p refunded!')
                    print('Bye!')
                    keep_buying = False
                    break
                else:
                    break
            else:
                raise ValueError
        except ValueError:
            print('invalid selection')
    print()
    while keep_buying:
        if VendingMachine.new_balance == 0:
            print()
            print('*******RECEIPT*******')
            vm.date()
            # the list comprehension flattened a list of list to a single a list
            new_cart = [item for sublist in VendingMachine.cart for item in sublist]
            # numpy is used to unpack the list
            cart = dict(zip(*np.unique(new_cart, return_counts=True)))
            cart_df = pd.DataFrame(list(cart.items()), columns=['Products', 'Qty'])
            cart_df.index += 1
            print(f'\n{cart_df}')
            print('See you again!')
            print(20 * '*')
            keep_buying = False
        else:
            print()
            vm.menu_list()
            to_cancel = ['y', 'n']
            while True:
                try:
                    # cancel variable here allows the user to end or keep adding to the cart
                    # so long as his/her coin could still afford it
                    cancel = input('Press "y" to add an item to cart\nPress "n" to end transaction >>> ').lower()
                    if cancel in to_cancel:
                        if cancel == 'n':
                            if VendingMachine.new_balance == VendingMachine.INSERTED_COIN:
                                print(f'{VendingMachine.INSERTED_COIN}p refunded.')
                            elif VendingMachine.new_balance > 0:
                                print()
                                print('*******RECEIPT*******')
                                vm.date()
                                # the list comprehension flattened a list of list to a single a list
                                new_cart = [item for sublist in VendingMachine.cart for item in sublist]
                                # numpy is used to unpack the list
                                cart = dict(zip(*np.unique(new_cart, return_counts=True)))
                                cart_df = pd.DataFrame(list(cart.items()), columns=['Products', 'Qty'])
                                cart_df.index += 1
                                print(f'\n{cart_df}')
                                print(f'Your change is {VendingMachine.new_balance}p')
                                print('Cheers!')
                                print(20 * '*')
                            keep_buying = False
                            break
                        elif cancel == 'y':
                            vm.select_choc()
                            vm.quantity()
                            break
                    else:
                        raise ValueError
                except ValueError:
                    print('invalid character')


vend()



