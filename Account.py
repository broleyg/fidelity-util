import json

from Position import Position
from Transaction import Transaction
from Strategy import Strategy

class Account:

    def __init__(self):

        self.id = ""
        self.__initial_balance = 0
        self.__current_balance = 0
        self.__strategies = []
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
    def initial_balance(self):
        return self.__initial_balance

    @initial_balance.setter
    def initial_balance(self, new_quantity):
        try:
            value = float(Position.currency_value(new_quantity))
        except ValueError as e:
            if new_quantity == '':
                value = 0.00
            else:
                raise ValueError("Inavlid initial balance {}".format(new_quantity))

        self.__initial_balance = value

    @property
    def current_balance(self):
        self.update_account()
        return self.__current_balance

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

    @property
    def strategies(self):
        return self.__strategies

    @strategies.setter
    def strategies(self, strategies):
        self.__strategies = strategies


    def add_transactions(self, txns):
        for txn in txns:
            try:
                self.add_transaction(txn)
            except ValueError as e:
                print("Fail to add transaction {}: {}".format(txn, e))

    def add_transaction(self, txn):
        if isinstance(txn, Transaction) and (txn.symbol != ''):
            self.transactions.append(txn)
            self.transactions.sort(key=lambda x: x.date)
            self.add_to_position(txn)
        else:
            raise ValueError("A valid transaction must be provided")


    def add_to_position(self, txn):
        if isinstance(txn, Transaction):
            if txn.symbol in self.__psns:
                pos = self.__psns[txn.symbol]
            else:
                pos = Position()
                pos.symbol = txn.symbol
                self.__psns[txn.symbol] = pos
            pos.add_transaction(txn)
        else:
            raise ValueError("A valid position must be provided")

    def update_account(self):
        self.__current_balance = self.__initial_balance
        for symbol, pos in self.positions.items():
            self.__current_balance = self.__current_balance + pos.amount

    def get_transactions_for_symbol(self, symbol):
        txns  = []
        for txn in self.transactions:
            if txn.symbol == symbol:
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
