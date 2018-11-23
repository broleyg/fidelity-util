import re
from datetime import date

class Transaction:

    BUY = 1
    SELL = -1
    NONE = 0

    CALL = "C"
    PUT = "P"

    # Step #1 for a Class - always create an __init__ method
    def __init__(self):
        self.id = ""

        self.symbol = ""
        self.description = ""
        self.date = ""
        self.settlement_date = ""

        self.__is_option = False
        self.__option_type = None
        self.__option_symbol = ""
        self.__option_strike_price = 0.00
        self.__option_expiration_date = ""

        self.action = Transaction.NONE

        # The following  member variables need specialized setters
        # to enforce positive number only rules, and they all can
        # be fractional
        self.shares = 0
        self.price = 0.00
        self.commission = 0.00
        self.fees = 0.00
        self.amount = 0.00

    def __str__(self):
        return "transaction: {} {} {} {} {}".format(self.date, self.action, self.symbol, self.amount, self.price)

    # Handy article to show how to use private variables w getters and setters
    # https://www.python-course.eu/python3_properties.php

    @property
    def action(self):
        return self.__action

    @action.setter
    def action(self, action):
        if action == Transaction.NONE:
            self.__action = Transaction.NONE
        elif action == Transaction.SELL:
            self.__action = Transaction.SELL
        elif action == Transaction.BUY:
            self.__action = Transaction.BUY
        else:
            self.__action = Transaction.NONE
            raise ValueError("A transaction action must be either Buy or Sell.")

    @property
    def shares(self):
        return self.__shares

    @shares.setter
    def shares(self, shares):
        if shares < 0:
            self.__shares = 0
            raise ValueError("The number of shares for a transaction must be greater than zero.")
        else:
            self.__shares = shares

    @property
    def price(self):
        return self.__price

    @price.setter
    def price(self, price):
        if price < 0:
            self.__price = 0
            raise ValueError("The price paid per share for a transaction must be greater than zero.")
        else:
            self.__price = price

    @property
    def fees(self):
        return self.__fees

    @fees.setter
    def fees(self, fees):
        if fees < 0:
            self.__fees = 0
            raise ValueError("Any fees for the transaction must be greater than zero.")
        else:
            self.__fees = fees

    @property
    def commission(self):
        return self.__commission

    @commission.setter
    def commission(self, commission):
        if commission < 0:
            self.__commission = 0
            raise ValueError("Any commission for the transaction must be greater than zero.")
        else:
            self.__commission = commission

    @property
    def amount(self):
        return self.__amount

    @amount.setter
    def amount(self, amount):
        if amount < 0:
            self.__amount = 0
            raise ValueError("The total price for the transaction must be greater than zero.")
        else:
            self.__amount = amount

    @property
    def symbol(self):
       return self.__symbol

    @symbol.setter
    def symbol(self, new_symbol):
        if new_symbol is None:
           self.__symbol = ""
           self.__option_type = False

        else:
            matches = re.search("-(?P<symbol>[A-Z]*)(?P<exp_year>\d{2})(?P<exp_mon>\d{2})(?P<exp_day>\d{2})(?P<opt_type>[CP])(?P<strike_price>\d*\.?\d*)", new_symbol)

            if matches is None:
                self.__symbol = new_symbol
                self.__option_type = False

            else:
                self.__is_option = True
                self.__option_symbol = new_symbol[1:]

                underlying_symbol = matches.group('symbol')
                if underlying_symbol == '':
                    raise AttributeError('The underlying symbol was not found in the option symbol')
                else:
                    self.__symbol = underlying_symbol

                exp_yr = int('20' + matches.group('exp_year'))
                exp_mo = int(matches.group('exp_mon'))
                exp_day = int(matches.group('exp_day'))
                try:
                    exp_date = date(exp_yr, exp_mo, exp_day)
                except ValueError as e:
                    raise AttributeError("Invalid expiration date: {}".format(e))
                self.__option_expiration_date = exp_date

                opt_type = matches.group('opt_type')
                if (opt_type == Transaction.CALL) or (opt_type == Transaction.PUT):
                    self.__option_type = opt_type
                else:
                    raise AttributeError("An option type must be a 'C' (CALL) or a 'P' (PUT)")

                price = matches.group('strike_price')
                if price == '':
                    raise AttributeError("Invalid or missing option price {}".format(price))
                else:
                    self.__option_strike_price = float(price)


    @property
    def is_option(self):
        return self.__is_option

    @is_option.setter
    def is_option(self, option):
        raise ValueError("is_option flag is read only")

    @property
    def option_type(self):
        return self.__option_type

    @property
    def option_symbol(self):
        return self.__option_symbol

    @property
    def option_expiration_date(self):
        return self.__option_expiration_date

    @property
    def option_strike_price(self):
        return self.__option_strike_price


if __name__ == "__main__":
    txn = Transaction()
    txn.action = Transaction.SELL
    txn.symbol = "SWKS"
    txn.description = ""
    txn.date = "Nov 18 2018"
    txn.settlement_date = "Nov 21 2018"

    txn.shares = 100
    txn.commission = 5.95
    txn.fees = 0.00
    txn.price = 95.25
    txn.amount = 9519.05

    print (txn)
