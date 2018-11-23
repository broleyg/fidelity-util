from unittest import TestCase
from Transaction import Transaction

class TestTransaction(TestCase):
    def setUp(self):
        self.txn = Transaction()

class TestInit(TestTransaction):

    def test_initial_action(self):
        self.assertEqual(self.txn.action, Transaction.NONE)

    def test_initial_symbol(self):
        self.assertEqual(self.txn.symbol, "")

    def test_initial_description(self):
        self.assertEqual(self.txn.description, "")

    def test_initial_date(self):
        self.assertEqual(self.txn.date, "")

    def test_initial_settlement_date(self):
        self.assertEqual(self.txn.settlement_date, "")

    def test_initial_shares(self):
        self.assertEqual(self.txn.shares, 0)

    def test_initial_price(self):
        self.assertEqual(self.txn.price, 0.00)

    def test_initial_commission(self):
        self.assertEqual(self.txn.commission, 0.00)

    def test_initial_fees(self):
        self.assertEqual(self.txn.fees, 0.00)

    def test_initial_amount(self):
        self.assertEqual(self.txn.amount, 0)

class TestPrice(TestTransaction):
    def setUp(self):
        self.txn = Transaction()

    def test_valid_price(self):
        test_price = 12.01
        self.txn.price = test_price
        self.assertEqual(self.txn.price, test_price)

    def test_invalid_price(self):
        test_price = -12.01
        try:
            self.txn.price = test_price
            self.failIfEqual(self.txn.price, test_price)
        except ValueError as e:
            self.assertEqual(self.txn.price, 0)


class TestShares(TestTransaction):
    def setUp(self):
        self.txn = Transaction()

    def test_valid_shares(self):
        test_shares = 12.01
        self.txn.shares = test_shares
        self.assertEqual(self.txn.shares, test_shares)

    def test_invalid_shares(self):
        test_shares = -12.01
        try:
            self.txn.shares = test_shares
            self.failIfEqual(self.txn.shares, test_shares)
        except ValueError as e:
            self.assertEqual(self.txn.shares, 0)


class TestCommission(TestTransaction):
    def setUp(self):
        self.txn = Transaction()

    def test_valid_commission(self):
        test_commission = 12.01
        self.txn.commission = test_commission
        self.assertEqual(self.txn.commission, test_commission)

    def test_invalid_commission(self):
        test_commission = -12.01
        try:
            self.txn.commission = test_commission
            self.failIfEqual(self.txn.commission, test_commission)
        except ValueError as e:
            self.assertEqual(self.txn.commission, 0)

class TestFees(TestTransaction):
    def setUp(self):
        self.txn = Transaction()

    def test_valid_fees(self):
        test_fees = 12.02
        self.txn.fees = test_fees
        self.assertEqual(self.txn.fees, test_fees)

    def test_invalid_fees(self):
        test_fees = -12.01
        try:
            self.txn.fees = test_fees
            self.failIfEqual(self.txn.fees, test_fees)
        except ValueError as e:
            self.assertEqual(self.txn.fees, 0)

class TestAmount(TestTransaction):
    def setUp(self):
        self.txn = Transaction()

    def test_valid_amount(self):
        test_amount = 100
        self.txn.amount = test_amount
        self.assertEqual(self.txn.amount, test_amount)

    def test_invalid_amount(self):
        test_amount = -3
        try:
            self.txn.amount = test_amount
            self.failIfEqual(self.txn.amount, test_amount)
        except ValueError as e:
            self.assertEqual(self.txn.amount, 0)


class TestAction(TestTransaction):
    def setUp(self):
        self.txn = Transaction()

    def test_sell_action(self):
        test_action = Transaction.SELL
        self.txn.action = test_action
        self.assertEqual(self.txn.action, test_action)

    def test_buy_action(self):
        test_action = Transaction.BUY
        self.txn.action = test_action
        self.assertEqual(self.txn.action, test_action)

    def test_invalid_action(self):
        test_action = "blah"
        try:
            self.txn.action = test_action
            self.failIfEqual(self.txn.action, test_action)
        except ValueError as e:
            self.assertEqual(self.txn.action, "")
