from unittest import TestCase
from Account import Account
from Transaction import Transaction


class TestAccount(TestCase):
    def setUp(self):
        act = Account()


class TestInit(TestAccount):
    def test_initial_id(self):
        self.assertEqual(self.act.id, "")

    def test_initial_balance(self):
        self.assertEqual(self.act.balance, 0.00)

    def test_initial_transactions(self):
        self.assertEqual(self.act.transactions.count, 0)


class TestId(TestAccount):
    def test_id(self):
        test_id = "IRA"
        self.act.id = test_id
        self.assertEqual(self.act.id, test_id)


