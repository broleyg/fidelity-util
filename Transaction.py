import re
from datetime import date
import locale

class Transaction:

    BUY = "BUY"
    SELL = "SELL"
    NONE = "NONE"

    CALL = "C"
    PUT = "P"

    # Step #1 for a Class - always create an __init__ method
    def __init__(self):
        self.id = ""

        self.symbol = ""
        self.description = ""
        self.date = ""
        self.settlement_date = ""
        self.funds_type = ''
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
        self.__amount = 0.00

    def __str__(self):
        return "<{} {} {} {} @ {} (minus {} and {}) = {} ".format(self.date, self.action, self.symbol, self.shares, self.price, self.fees, self.commission, self.amount)

    # Handy article to show how to use private variables w getters and setters
    # https://www.python-course.eu/python3_properties.php

    @property
    def action(self):
        return self.__action

    @action.setter
    def action(self, action):

        match = re.search(r"(BUY|BOUGHT)", action)
        if match:
            self.__action = Transaction.BUY
            return

        match = re.search(r"(SELL|SOLD)", action)
        if match:
            self.__action = Transaction.SELL
            return

        self.__action = action
        #self.__action = Transaction.NONE

    @property
    def shares(self):
        return self.__shares

    @shares.setter
    def shares(self, shares):
        try:
            value = float(self.__currency_value(shares))
        except ValueError as e:
            if shares == '':
                value = 0.00
            else:
                raise ValueError("Inavlid shares {}".format(shares))

        self.__shares = value


    def __currency_value(self, value):
        if isinstance(value, str):
            locale.setlocale(locale.LC_ALL, '')
            conv = locale.localeconv()
            no_currency = value.replace(conv['currency_symbol'], '')
            raw_numbers = no_currency.replace(conv['thousands_sep'], '')
            return raw_numbers

        return value


    @property
    def price(self):
        return self.__price

    @price.setter
    def price(self, price):
        try:
            value = float(self.__currency_value(price))
        except ValueError as e:
            if price == '':
                value = 0.00
            else:
                raise ValueError("Invalid price {}".format(price))

        self.__price = value
        #if value < 0:
        #    self.__price = 0
        #    raise ValueError("The price paid per share for a transaction must be greater than zero.")
        #else:
        #    self.__price = value

    @property
    def fees(self):
        return self.__fees

    @fees.setter
    def fees(self, fees):
        try:
            value = float(self.__currency_value(fees))
        except ValueError as e:
            if fees == '':
                value = 0.0
            else:
                raise ValueError("Invalid fees {}".format(fees))

        if value < 0:
            self.__fees = 0
            raise ValueError("Any fees for the transaction must be greater than zero.")
        else:
            self.__fees = value

    @property
    def commission(self):
        return self.__commission

    @commission.setter
    def commission(self, commission):
        try:
            value = float(self.__currency_value(commission))
        except ValueError as e:
            if commission == '':
                value = 0.0
            else:
                raise ValueError("Invalid commission {}".format(commission))

        if value < 0:
            self.__commission = 0
            raise ValueError("Any commission for the transaction must be greater than zero.")
        else:
            self.__commission = value

    @property
    def amount(self):
        return self.__amount

    @amount.setter
    def amount(self, amount):
        try:
            value = float(self.__currency_value(amount))
        except ValueError as e:
            if amount == '':
                value = 0.0
            else:
                raise ValueError("Invalid amount {}".format(amount))

        self.__amount = value

        #if value < 0:
        #    self.__amount = 0
        #    raise ValueError("The total price for the transaction must be greater than zero.")
        #else:
        #    self.__amount = value

    @property
    def symbol(self):
       return self.__symbol

    @symbol.setter
    def symbol(self, new_symbol):

        # First, ensure that we have a value provided, to avoid all the costly regular expression searching
        if new_symbol is None:
           self.__symbol = ''
           self.__option_symbol == ''
           self.__is_option = False

        # .. so now that we know have a value ...
        else:

            # Lets check and see if it's an option symbol, which has the following format
            #
            #  -SWKS180132P105.50
            match = re.search("(?P<option_flag>\-)(?P<symbol>[A-Z]*)(?P<exp_year>\d{2})(?P<exp_mon>\d{2})(?P<exp_day>\d{2})(?P<opt_type>[A-Z])(?P<strike_price>\d*\.?\d*)", new_symbol)

            if match:

                self.__is_option = (match.group('option_flag') == '-')

                underlying_symbol = match.group('symbol')
                if underlying_symbol == '':
                    raise AttributeError('The underlying symbol was not found in the option symbol')
                else:
                    self.__symbol = underlying_symbol
                self.__option_symbol = new_symbol[1:]


                exp_yr = int('20' + match.group('exp_year'))
                exp_mo = int(match.group('exp_mon'))
                exp_day = int(match.group('exp_day'))
                try:
                    exp_date = date(exp_yr, exp_mo, exp_day)
                except ValueError as e:
                    raise AttributeError("Invalid expiration date: {}".format(e))
                self.__option_expiration_date = exp_date

                opt_type = match.group('opt_type')
                if (opt_type == Transaction.CALL) or (opt_type == Transaction.PUT):
                    self.__option_type = opt_type
                else:
                    raise AttributeError("An option type must be a 'C' (CALL) or a 'P' (PUT)")

                price = match.group('strike_price')
                if price == '':
                    raise AttributeError("Invalid or missing option price {}".format(price))
                else:
                    self.__option_strike_price = float(price)

            else:

                if new_symbol[0:1] == '-':
                    raise AttributeError('Invalid option symbol {}'.format(new_symbol))

                else:
                    self.__symbol = new_symbol
                    self.__option_symbol = ''
                    self.__is_option = False


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
