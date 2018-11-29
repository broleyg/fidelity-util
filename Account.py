from Transaction import Transaction
from Position import Position
import json
import copy

class Account:

    def __init__(self):

        self.id = ""
        self.balance = 0
        self.__psns = {}
        self.__txns = []

    def __str__(self):
        rep = {}
        for key, value in self.__dict__.items():
            if key[:1] == '_':
                attr = key[10:]
            else:
                attr = key
            rep[attr] = value
        return json.dumps(rep, indent=4, sort_keys=True, default=str)

    @property
    def transactions(self):
        return self.__txns

    @transactions.setter
    def transactions(self, transactions):
        self.__txns = transactions

    def add_transaction(self, txn):
        if isinstance(txn, Transaction):
            self.transactions.append(txn)
            self.add_position(txn)
        else:
            raise ValueError("A valid transaction must be provided")

    def add_position(self, pos):
        if isinstance(pos, Position):
            if pos.symbol in self.__psns:
                p = self.__psns[pos.symbol]
                p.quantity = p.quantity + pos.quantity
            else:
                new_pos = Position()
                new_pos.symbol = pos.symbol
                new_pos.description = pos.description
                new_pos.quantity = pos.quantity
                self.__psns[pos.symbol] = new_pos
        else:
            raise ValueError("A valid position must be provided")

if __name__ == "__main__":
    act = Account()
    act.id = "IRA"
    act.balance = "100.00"

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

    act.transactions.append(txn)

    print (act)
