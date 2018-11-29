from unittest import TestCase
from Account import Account
from Transaction import Transaction


class TestAccount(TestCase):
    def setUp(self):
        self.act = Account()


class TestInit(TestAccount):
    def test_initial_id(self):
        self.assertEqual(self.act.id, "")

    def test_initial_balance(self):
        self.assertEqual(self.act.balance, 0.00)

    def test_initial_transactions(self):
        self.assertEqual(len(self.act.transactions), 0)


class TestId(TestAccount):
    def test_id(self):
        test_id = "IRA"
        self.act.id = test_id
        self.assertEqual(self.act.id, test_id)

class TestTransactions(TestAccount):
    def test_add_transaction(self):
        txn = Transaction()

        txn.symbol = "SWKS"
        txn.description = ""
        txn.quantity= 100

        txn.action = Transaction.SELL
        txn.commission = 5.95
        txn.fees = 0.00
        txn.price = 95.25
        txn.amount = 9519.05
        txn.date = "11/18/2018"
        txn.settlement_date = "11/19/2018"

        self.act.add_transaction(txn)
        self.assertIn(txn, self.act.transactions)
        print (self.act)

    def test_add_two_transaction(self):
        self.test_add_transaction()
        self.test_add_transaction()
        print (self.act)

