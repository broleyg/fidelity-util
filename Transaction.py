import re

from Security import Security

class Transaction(Security):

    BUY = 'BUY'
    SELL = 'SELL'
    EXPIRED = 'EXPIRED'
    ASSIGNED = 'ASSIGNED'
    DIVIDEND = 'DIVIDEND'
    REINVEST = 'REINVEST'
    NONE = 'NONE'

    # Step #1 for a Class - always create an __init__ method
    def __init__(self):
        super().__init__()
        self.id = ""
        self.action = Transaction.NONE
        self.__date = ""
        self.__settlement_date = ""
        self.funds_type = ''
        self.price = 0.00
        self.commission = 0.00
        self.fees = 0.00
        self.__amount = 0.00
        self.__cash_reserved = 0.00

    # Handy article to show how to use private variables w getters and setters
    # https://www.python-course.eu/python3_properties.php

    @property
    def date(self):
        return self.__date

    @date.setter
    def date(self, date):
        self.__date = Transaction.date_value(date)

    @property
    def settlement_date(self):
        return self.__settlement_date

    @settlement_date.setter
    def settlement_date(self, settlement_date):
        self.__settlement_date = Transaction.date_value(settlement_date)

    @property
    def action(self):
        return self.__action

    @action.setter
    def action(self, new_action):
        new_action = new_action.upper()

        match = re.search(r"(BUY|BOUGHT|PURCHASE)", new_action)
        if match:
            self.__action = Transaction.BUY
            return

        match = re.search(r"(SELL|SOLD|REDEMPTION)", new_action)
        if match:
            self.__action = Transaction.SELL
            return

        match = re.search(r"(EXPIRE)", new_action)
        if match:
            self.__action = Transaction.EXPIRED
            return

        match = re.search(r"(ASSIGN)", new_action)
        if match:
            self.__action = Transaction.ASSIGNED
            return

        match = re.search(r"(DIVIDEND|CAP GAIN|IN LIEU OF)", new_action)
        if match:
            self.__action = Transaction.DIVIDEND
            return

        match = re.search(r"(REINVEST)", new_action)
        if match:
            self.__action = Transaction.REINVEST
            return

        self.__action = new_action
        #self.__action = Transaction.NONE

    @property
    def price(self):
        return self.__price

    @price.setter
    def price(self, price):
        try:
            value = float(Transaction.currency_value(price))
        except ValueError as e:
            if price == '':
                value = 0.00
            else:
                raise ValueError("Invalid price {}".format(price))

        self.__price = value

    @property
    def fees(self):
        return self.__fees

    @fees.setter
    def fees(self, fees):
        try:
            value = float(Transaction.currency_value(fees))
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
            value = float(Transaction.currency_value(commission))
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
            value = float(Transaction.currency_value(amount))
        except ValueError as e:
            if amount == '':
                value = 0.0
            else:
                raise ValueError("Invalid amount {}".format(amount))

        self.__amount = value


    @property
    def cash_reserved(self):
        if self.is_option:
            if self.action == Transaction.SELL and self.option_type == Transaction.PUT:
                return self.quantity * self.option_strike_price * 100
        return 0.00

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
