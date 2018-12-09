import json
import re
from datetime import date

from Security import Security
from Transaction import Transaction


class Position(Security):

    def __init__(self):
        super().__init__()
        self.transactions=[]
        self.__reset_calculated_fields()


    def __reset_calculated_fields(self):
        self.__is_open = True
        self.__open_date = None
        self.__close_date = None
        self.__valid_date_range = False
        self.__position_length = 0
        self.__realized_gain = 0.0
        self.__unrealized_gain = 0.0
        self.__open_quantity = 0.0
        self.__basis = 0.0


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

    @property
    def amount(self):
        return (self.realized_gain + self.unrealized_gain)

    @property
    def realized_gain(self):
        return self.__realized_gain

    @property
    def unrealized_gain(self):
        return self.__unrealized_gain

    @property
    def basis(self):
        return self.__basis

    @property
    def roi(self):
        if self.basis != 0:
            return (self.amount / self.basis * 100) * -1.0
        else:
            return 0.00

    @property
    def annualized_roi(self):
        value = self.roi
        rate = 365 / self.position_length
        return value * rate

    # @amount.setter
    # def amount(self, amount):
    #     try:
    #         value = float(Transaction.currency_value(amount))
    #     except ValueError as e:
    #         if amount == '':
    #             value = 0.0
    #         else:
    #             raise ValueError("Invalid amount {}".format(amount))
    #
    #     self.__realized_gain = value

    def add_transaction(self, txn):
        txns = []
        txns.append(txn)
        self.add_transactions(txns)

    def add_transactions(self, txns):
        for txn in txns:
            if (txn is None) or (txn.symbol is None) or (txn.symbol == ''):
                raise ValueError('Invalid transaction: {}'.format(txn))

            if (self.symbol is None) or (self.symbol == ''):
                self.symbol = txn.symbol

            if (txn.symbol == self.symbol):
                self.transactions.append(txn)
            else:
                if txn.is_option:
                    raise ValueError("The option {} does not match the underlying security {}".format(txn.symbol, self.symbol))
                else:
                    raise ValueError("The transaction {} does not match the security {}".format(txn.symbol, self.symbol))

        #self.update()

    def update(self):
        self.__reset_calculated_fields()
        self.transactions.sort(key=lambda x: x.date)

        open_date = self.transactions[0].date
        close_date = self.transactions[len(self.transactions)- 1].date

        if self.transactions[0].action == Transaction.BUY:
            self.__basis = self.transactions[0].amount
        else:
            self.__basis = self.transactions[0].cash_reserved

        #print ('Updating positon = {}'.format(self.symbol))
        for txn in self.transactions:
            #print ('\t txn amount = {}, quantity = {}'.format(txn.amount, txn.quantity))
            self.quantity = self.quantity + txn.quantity
            self.__realized_gain = self.__realized_gain + txn.amount
            self.__is_open = (self.quantity != 0)
            #print ('\t position realized gains = {}, quantity = {}'.format(self.__realized_gain, self.quantity))

        if self.is_open:
            self.open_date = open_date
            self.close_date = date.today()

            try:
                if self.is_option:
                    if self.option_expiration_date >= date.today():
                        price = self.current_quote
                        self.__unrealized_gain = self.quantity * price * 100
                else:
                    price = self.current_quote
                    self.__unrealized_gain = self.quantity * price

            except Exception as e:
                print('Unable to find quote for symbol {}'.format(self.symbol))
                #raise ValueError('Unable to find quote for symbol {}'.format(self.symbol))

        else:
            self.open_date = open_date
            self.close_date = close_date


