import json

from Security import Security
from Position import Position

class Strategy(Position):

    def __init__(self):
        self.__positions = {}


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


    def add_position(self, pos):
        if pos is None or not isinstance(pos, Position):
            raise ValueError('A valid position must be provided')

        if (pos.underlying_symbol is None) or (pos.underlying_symbol == ''):
            raise ValueError('The position to add does not have a valid symbol')

        if (self.underlying_symbol is None) or (self.underlying_symbol == ''):
            self.symbol = pos.underlying_symbol

        if (pos.underlying_symbol == self.underlying_symbol):
            self.transactions.append(pos)
            self.update()
        else:
            if pos.is_option:
                raise ValueError("The option {} does not match the underlying security {}".format(pos.underlying_symbol, self.underlying_symbol))
            else:
                raise ValueError("The transaction {} does not match the security {}".format(pos.underlying_symbol, self.underlying_symbol))

    def update(self):
        return

