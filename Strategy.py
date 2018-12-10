import json

from datetime import date

from Security import Security
from Transaction import Transaction
from Position import Position

class Strategy(Position):

    def __init__(self):
        self.__positions = {}
        self.__realized_gain = 0.00
        self.__unrealized_gain = 0.00
        self.__basis = 0.00
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

    # def add_transaction(self, txn):
    #     txns = []
    #     txns.append(txn)
    #     self.add_transactions(txns)

    def add_transactions(self, txns):
        for txn in txns:
            if Position.is_valid_transaction(txn):

                if (self.underlying_symbol is None) or (self.underlying_symbol == ''):
                    self.symbol = txn.underlying_symbol

                else:
                    if txn.underlying_symbol != self.underlying_symbol:
                        if txn.is_option:
                            raise ValueError("The option {} does not match the underlying Strategy security {}".format(txn.underlying_symbol, self.underlying_symbol))
                        else:
                            raise ValueError("The transaction {} does not match the Strategy security {}".format(txn.underlying_symbol, self.underlying_symbol))

                if txn.symbol in self.__positions:
                    pos = self.__positions[txn.symbol]

                else:
                    pos = Position()
                    self.__positions[txn.symbol] = pos
                    pos.symbol = txn.symbol

                pos.add_transaction(txn)


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
        open_date = date.today()
        close_date = date.today()

        for symbol, pos in self.__positions.items():
            pos.update()


            self.__realized_gain = self.__realized_gain + pos.realized_gain
            self.__unrealized_gain = self.__unrealized_gain + pos.unrealized_gain
            self.__basis = self.__basis + pos.basis

            if pos.open_date < open_date:
                open_date = pos.open_date

