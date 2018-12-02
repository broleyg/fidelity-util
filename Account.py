from Transaction import Transaction
from Position import Position
import json


class Account:

    def __init__(self):

        self.id = ""
        self.balance = 0
        self.__psns = {}
        self.__txns = []

    def __str__(self):
        rep = {}
        for key, value in self.__dict__.items():
            pos = key.rfind('_')
            if pos > 0:
                attr = key[pos+1:]
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

    @property
    def positions(self):
        return self.__psns

    @positions.setter
    def positions(self, positions):
        self.__psns = positions

    def add_transactions(self, txns):
        for txn in txns:
            try:
                self.add_transaction(txn)
            except ValueError as e:
                print("Fail to add transaction: {}".format(txn))

    def add_transaction(self, txn):
        if isinstance(txn, Transaction) and (txn.symbol != ''):
            self.transactions.append(txn)
            self.add_to_position(txn)
        else:
            raise ValueError("A valid transaction must be provided")

    def start_position(self, pos):
        return

    def update_position(self, txn):

        return

    def add_to_position(self, txn):
        if isinstance(txn, Transaction):
            if txn.symbol in self.__psns:
                p = self.__psns[txn.underlying_symbol]
                if txn.action == Transaction.BUY:
                    p.quantity = p.quantity + txn.quantity
                elif txn.action == Transaction.SELL:
                    p.quantity = p.quantity - txn.quantity
                    p.open = not (p.quantity == 0)

            else:
                new_pos = Position()
                new_pos.symbol = txn.symbol
                #new_pos.description = pos.description
                new_pos.quantity = txn.quantity
                self.__psns[txn.underlying_symbol] = new_pos
        else:
            raise ValueError("A valid position must be provided")


    def get_transactions_for_symbol(self, symbol):
        txns  = []
        for txn in self.transactions:
            if txn.underlying_symbol == symbol:
                txns.append(txn)
        txns.sort(key=lambda x: x.date)
        return txns


    def get_total_amount_for_symbol(self, symbol):
        total_amount = 0.0
        txns = self.get_transactions_for_symbol(symbol)
        for txn in txns:
            total_amount = total_amount + txn.amount
        return total_amount

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
