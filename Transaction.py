import re
import datetime
import locale
import json

from Position import Position

class Transaction(Position):

    BUY = "BUY"
    SELL = "SELL"
    NONE = "NONE"

    locale.setlocale(locale.LC_ALL, '')
    __conv = locale.localeconv()

    # Step #1 for a Class - always create an __init__ method
    def __init__(self):

        self.id = ""
        self.action = Transaction.NONE
        self.__date = ""
        self.__settlement_date = ""
        self.funds_type = ''
        self.price = 0.00
        self.commission = 0.00
        self.fees = 0.00
        self.__amount = 0.00

    def __str__(self):
        rep = {}
        for key, value in self.__dict__.items():
            pos = key.rfind('__')
            if pos > 0:
                attr = key[pos+2:]
            else:
                attr = key
            rep[attr] = value
        return json.dumps(rep, indent=4, sort_keys=True, default=str)

    def __currency_value(self, value):
        if isinstance(value, str):
            no_currency = value.replace(self.__conv['currency_symbol'], '')
            raw_numbers = no_currency.replace(self.__conv['thousands_sep'], '')
            return raw_numbers
        else:
            return value

    def __date_value(self, value):
        if isinstance(value, str) and (value.strip() != ''):
            format = locale.nl_langinfo(locale.D_FMT)
            date_value = datetime.datetime.strptime(value.strip(), format).date()
            return date_value
        elif isinstance(value, datetime.date):
            return value
        else:
            return None


    # Handy article to show how to use private variables w getters and setters
    # https://www.python-course.eu/python3_properties.php

    @property
    def date(self):
        return self.__date

    @date.setter
    def date(self, date):
        self.__date = self.__date_value(date)

    @property
    def settlement_date(self):
        return self.__settlement_date

    @settlement_date.setter
    def settlement_date(self, settlement_date):
        self.__settlement_date = self.__date_value(settlement_date)

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


if __name__ == "__main__":
    txn = Transaction()
    txn.action = Transaction.SELL
    txn.date = "11/18/2018"

    txn.symbol = "SWKS"
    txn.description = ""

    txn.quantity= 100
    txn.commission = 5.95
    txn.fees = 0.00
    txn.price = 95.25
    txn.amount = 9519.05

    txn.settlement_date = "11/19/2018"

    print (txn)
