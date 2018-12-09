import json

from Security import Security
from Transaction import Transaction
from Position import Position

class Strategy(Position):

    def __init__(self):
        self.__positions = {}
        super().__init__()

    # @property
    # def open_date(self):
    #     return super().open_date
    #
    # @open_date.setter
    # def open_date(self, date):
    #     super().open_date = date
    #
    # @property
    # def close_date(self):
    #     return self.__close_date
    #
    # @close_date.setter
    # def close_date(self, date):
    #     self.__close_date = Transaction.date_value(date)
    #     self.__calculate_days_open()
    #
    # @property
    # def is_open(self):
    #     return self.__is_open
    #
    # @property
    # def is_valid_date_range(self):
    #     return self.__valid_date_range
    #
    # @property
    # def position_length(self):
    #     return self.__position_length
    #
    # @property
    # def amount(self):
    #     return (self.realized_gain + self.unrealized_gain)
    #
    # @property
    # def realized_gain(self):
    #     return self.__realized_gain
    #
    # @property
    # def unrealized_gain(self):
    #     return self.__unrealized_gain
    #
    # @property
    # def basis(self):
    #     return self.__basis
    #
    # @property
    # def roi(self):
    #     if self.basis != 0:
    #         return (self.amount / self.basis * 100) * -1.0
    #     else:
    #         return 0.00
    #
    # @property
    # def annualized_roi(self):
    #     value = self.roi
    #     rate = 365 / self.position_length
    #     return value * rate

    def add_transaction(self, txn):
        if (txn is None) or (txn.underlying_symbol is None) or (txn.underlying_symbol == ''):
            raise ValueError('Invalid transaction: {}'.format(txn))

        if (self.underlying_symbol is None) or (self.underlying_symbol == ''):
            self.symbol = txn.underlying_symbol

        if (txn.underlying_symbol == self.underlying_symbol):
            self.transactions.append(txn)
            self.update()
        else:
            if txn.is_option:
                raise ValueError("The option {} does not match the underlying security {}".format(txn.underlying_symbol, self.underlying_symbol))
            else:
                raise ValueError("The transaction {} does not match the security {}".format(txn.underlying_symbol, self.underlying_symbol))


    # def add_position(self, pos):
    #     if pos is None or not isinstance(pos, Position):
    #         raise ValueError('A valid position must be provided')
    #
    #     if (pos.underlying_symbol is None) or (pos.underlying_symbol == ''):
    #         raise ValueError('The position to add does not have a valid symbol')
    #
    #     if (self.underlying_symbol is None) or (self.underlying_symbol == ''):
    #         self.symbol = pos.underlying_symbol
    #
    #     if (pos.underlying_symbol == self.underlying_symbol):
    #         self.transactions.append(pos)
    #         self.update()
    #     else:
    #         if pos.is_option:
    #             raise ValueError("The option {} does not match the underlying security {}".format(pos.underlying_symbol, self.underlying_symbol))
    #         else:
    #             raise ValueError("The transaction {} does not match the security {}".format(pos.underlying_symbol, self.underlying_symbol))

    def update(self):
        return

