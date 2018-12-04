import json
import re
from datetime import date
from decimal import *

from Security import Security
from Transaction import Transaction

class Position(Security):

    def __init__(self):
        super().__init__()
        self.transactions=[]
        self.__open={}
        self.__reset_calculated_fields()


    def __reset_calculated_fields(self):
        self.__is_open = True
        self.__open_date = None
        self.__close_date = None
        self.__valid_date_range = False
        self.__position_length = 0
        self.__amount = 0.0
        self.__open={}

    def ___validate_date_range(self):
        self.__valid_date_range = False

        if self.__open_date is None and self.__close_date is None:
            self.__valid_date_range = False

        elif self.__open_date is None and self.__close_date is not None:
            self.__valid_date_range = False
#            if self.__close_date > date.today():
#                raise ValueError('Invalid date range: open date is None and close date {} is in the future'.format(self.__close_date))

        elif self.__open_date is not None and self.__close_date is None:
            self.__valid_date_range = False
#            if self.__open_date > date.today():
#                raise ValueError('Invalid date range: open date {} is in the future and close date is None'.format(self.__open_date))
        else:
            if self.__close_date >= self.__open_date:
                self.__valid_date_range = True
            else:
                self.__valid_date_range = False
                raise ValueError('Invalid date range: open date {} and close date {}'.format(self.__open_date, self.__close_date))

    def __calculate_days_open(self):
        days = 0
        self.___validate_date_range()
        if self.__valid_date_range:
            delta = self.__close_date - self.__open_date
            # days = delta.total_seconds() / 60 / 60 / 24
            days = delta.days
            self.__position_length = days + 1
            #print('{}, {}, {}'.format(self.__open_date, self.__close_date, self.__position_length))


    @property
    def open_date(self):
        return self.__open_date

    @open_date.setter
    def open_date(self, date):
        self.__open_date = Transaction.date_value(date)
        self.__calculate_days_open()

    @property
    def close_date(self):
        return self.__close_date

    @close_date.setter
    def close_date(self, date):
        self.__close_date = Transaction.date_value(date)
        self.__calculate_days_open()

    @property
    def is_open(self):
        return self.__is_open

    @property
    def is_valid_date_range(self):
        return self.__valid_date_range

    @property
    def position_length(self):
        return self.__position_length

    def add_transactions(self, txns):
        for txn in txns:
            try:
                self.add_transaction(txn)
            except ValueError as e:
                print("Fail to add transaction: {}".format(txn))

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


    def add_transaction(self, txn):
        if (txn is None) or (txn.underlying_symbol is None) or (txn.underlying_symbol == ''):
            raise ValueError('Invalid transaction: {}'.format(txn))

        if (self.underlying_symbol is None) or (self.underlying_symbol == ''):
            self.symbol = txn.underlying_symbol

        if (txn.underlying_symbol == self.underlying_symbol):
            self.transactions.append(txn)
            self.update_position()
        else:
            if txn.is_option:
                raise ValueError("The option {} does not match the underlying security {}".format(txn.underlying_symbol, self.underlying_symbol))
            else:
                raise ValueError("The transaction {} does not match the security {}".format(txn.underlying_symbol, self.underlying_symbol))

    def update_position(self):
        self.__reset_calculated_fields()
        self.transactions.sort(key=lambda x: x.date)

        open_date = self.transactions[0].date
        close_date = self.transactions[len(self.transactions)- 1].date

        for txn in self.transactions:

            if txn.symbol not in self.__open:
                self.__open[txn.symbol] = txn.quantity
            else:
                self.__open[txn.symbol] = self.__open[txn.symbol] + txn.quantity

            if self.__open[txn.symbol] == 0:
                del self.__open[txn.symbol]


            self.amount = self.amount + txn.amount

            if txn.is_option:

                # Long Call (option to buy at strike price)
                if txn.action == Transaction.BUY and txn.option_type == Transaction.CALL:
                    self.quantity = self.quantity + txn.quantity

                # Insurance/Protection (option to sell at strike price)
                if txn.action == Transaction.BUY and txn.option_type == Transaction.PUT:
                    self.quantity = self.quantity + txn.quantity

                # Covered Call (obligation to sell at strike price)
                elif txn.action == Transaction.SELL and txn.option_type == Transaction.CALL:
                    self.quantity = self.quantity - txn.quantity
                    self.__is_open = not (self.quantity == 0)

                # Happy to buy at the strike  (obligation to buy at strike price)
                elif txn.action == Transaction.SELL and txn.option_type == Transaction.CALL:
                    self.quantity = self.quantity - txn.quantity
                    self.__is_open = not (self.quantity == 0)

                elif txn.action == Transaction.EXPIRED:
                    self.quantity = self.quantity - txn.quantity
                    self.__is_open = not (self.quantity == 0)

                elif txn.action == Transaction.ASSIGNED:
                    self.quantity = self.quantity - txn.quantity
                    self.__is_open = not (self.quantity == 0)
            else:

                if txn.action == Transaction.BUY:
                    self.quantity = self.quantity + txn.quantity

                elif txn.action == Transaction.SELL:
                    self.quantity = self.quantity - txn.quantity
                    self.__is_open = not (self.quantity == 0)

        if len(self.__open) == 0:
            self.open_date = open_date
            self.close_date = close_date
        else:
            self.open_date = open_date
            self.close_date = date.today()


