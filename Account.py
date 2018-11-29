from Transaction import Transaction
import json

class Account:

    def __init__(self):
        self.id
        self.balance = 0
        self.positions = {}
        self.transactions = []

    def __str__(self):
        rep = {}
        for key, value in self.__dict__.items():
            if key[:1] == '_':
                attr = key[14:]
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
        if isinstance(txn, "Transaction"):
            self.__tnxs.append(txn)
        else:
            raise ValueError("A valid transaction must be provided")

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
