from unittest import TestCase
from datetime import date
from datetime import timedelta
from Position import Position
from Transaction import Transaction

class TestPosition(TestCase):
    def setUp(self):
        self.pos = Position()

    def new_transaction(self,test_date = None, test_symbol = 'SWKS', test_price=100.00, test_quantity=100, test_commission = 4.95, test_fees = 0):
        txn = Transaction()
        txn.symbol = test_symbol
        txn.quantity= test_quantity
        txn.action = Transaction.BUY
        txn.commission = test_quantity
        txn.fees = test_fees
        txn.price = test_price
        txn.date = test_date
        txn.amount = (-1 * test_price * test_quantity) - test_commission - test_fees
        return txn

    def new_buy_transaction(self, test_date = None, test_symbol = 'SWKS', test_price=100.00, test_quantity=100, test_commission = 4.95, test_fees = 0):
        txn = self.new_transaction(test_date, test_symbol, test_price, test_quantity, test_commission, test_fees)
        txn.action = Transaction.BUY
        txn.amount = (-1 *test_price * test_quantity) - test_commission - test_fees
        return txn

    def new_sell_transaction(self, test_date = None, test_symbol = 'SWKS', test_price=100.00, test_quantity=100, test_commission = 4.95, test_fees = 0):
        txn = self.new_transaction(test_date, test_symbol, test_price, test_quantity, test_commission, test_fees)
        txn.action = Transaction.SELL
        txn.amount = (1 *test_price * test_quantity) - test_commission - test_fees
        return txn


class TestInit(TestPosition):

    def test_initial_symbol(self):
        self.assertEqual(self.pos.symbol, "")

    def test_initial_description(self):
        self.assertEqual(self.pos.description, "")

    def test_initial_quantity(self):
        self.assertEqual(self.pos.quantity, 0)

    def test_initial_open_date(self):
        self.assertIsNone(self.pos.open_date)

    def test_intial_close_date(self):
        self.assertIsNone(self.pos.close_date)


class TestOpenDate(TestPosition):

    def test_valid_open_date(self):
        test_date = '12/01/2018'
        self.pos.open_date = test_date
        self.assertEqual(self.pos.open_date, test_date)
        self.assertFalse(self.pos.is_valid_date_range)
        self.assertEqual(self.pos.position_length, 0)

    def test_valid_open_date(self):
        test_date = date.today()
        self.pos.open_date = test_date
        self.assertEqual(self.pos.open_date, test_date)
        self.assertFalse(self.pos.is_valid_date_range)
        self.assertEqual(self.pos.position_length, 0)

    def test_invalid_open_date(self):
        test_date = '-12x.01'
        try:
            self.pos.open_date = test_date
            self.failIfEqual(self.pos.open_date, test_date)
        except ValueError as e:
            self.assertIsNone(self.pos.open_date)
            self.assertFalse(self.pos.is_valid_date_range)
            self.assertEqual(self.pos.position_length, 0)


class TestClosedDate(TestPosition):

    def test_valid_close_date(self):
        test_date = '12/01/2018'
        self.pos.close_date = test_date
        self.assertEqual(self.pos.close_date, test_date)
        self.assertFalse(self.pos.is_valid_date_range)
        self.assertEqual(self.pos.position_length, 0)

    def test_valid_close_date(self):
        test_date = date.today()
        self.pos.close_date = test_date
        self.assertEqual(self.pos.close_date, test_date)
        self.assertFalse(self.pos.is_valid_date_range)
        self.assertEqual(self.pos.position_length, 0)

    def test_invalid_close_date(self):
        test_date = '-12x.01'
        try:
            self.pos.close_date = test_date
            self.failIfEqual(self.pos.close_date, test_date)
        except ValueError as e:
            self.assertIsNone(self.pos.close_date)
            self.assertFalse(self.pos.is_valid_date_range)
            self.assertEqual(self.pos.position_length, 0)


class TestDateRange(TestPosition):

    def test_valid_date_range(self):
        days = 30
        test_open_date = date.today() - timedelta(days)
        test_close_date = date.today()
        self.pos.open_date = test_open_date
        self.pos.close_date = test_close_date
        self.assertTrue(self.pos.is_valid_date_range)
        self.assertEqual(self.pos.position_length, 31)

    def test_invalid_date_range(self):
        days = 30
        test_open_date = date.today()
        test_close_date = date.today() - timedelta(days)
        try:
            self.pos.open_date = test_open_date
            self.pos.close_date = test_close_date
            self.failIf(self.pos.is_valid_date_range, True)
        except ValueError as e:
            self.assertFalse(self.pos.is_valid_date_range)
            self.assertEqual(self.pos.position_length, 0)


class TestAmount(TestPosition):

    def test_valid_amount(self):
        test_amount = 100
        self.pos.amount = test_amount
        self.assertEqual(self.pos.amount, test_amount)

    def test_invalid_amount(self):
        test_amount = "lx"
        try:
            self.pos.amount = test_amount
            self.failIfEqual(self.pos.amount, test_amount)
        except ValueError as e:
            self.assertEqual(self.pos.amount, 0)

class TestTransactions(TestPosition):
    def test_add_transaction(self):
        txn = Transaction()

        txn.symbol = "SWKS"
        txn.quantity= 100

        txn.action = Transaction.SELL
        txn.commission = 5.95
        txn.fees = 0.00
        txn.price = 95.25
        txn.amount = 9519.05
        txn.date = "11/18/2018"
        txn.settlement_date = "11/19/2018"

        self.pos.add_transaction(txn)
        self.assertEqual(self.pos.underlying_symbol, txn.symbol)
        self.assertIn(txn, self.pos.transactions)

    def test_add_multiple_transactions(self):
        txns = []

        test_symbol = 'SWKS'
        txn = Transaction()
        txn.symbol = test_symbol
        txn.quantity= 100
        txn.action = Transaction.BUY
        txn.commission = 5.95
        txn.fees = 0.00
        txn.price = 95.25
        txn.amount = -9530.95
        txns.append(txn)

        txn = Transaction()
        txn.symbol = test_symbol
        txn.quantity= 100
        txn.action = Transaction.SELL
        txn.commission = 5.95
        txn.fees = 0.00
        txn.price = 99.25
        txn.amount = 9919.05
        txns.append(txn)

        self.pos.add_transactions(txns)
        self.assertEqual(self.pos.underlying_symbol, test_symbol)
        self.assertEqual(len(self.pos.transactions), len(txns))

    def test_add_invalid_transaction(self):

        test_symbol = 'SWKS'
        txn = self.new_buy_transaction(test_symbol = 'swks', test_price=95.25)
        self.pos.add_transaction(txn)

        txn = self.new_sell_transaction(test_symbol = 'APPL', test_price=99.25)

        try:
            self.pos.add_transaction(txn)
            self.failIfEqual(len(self.pos.transactions), 2)
        except ValueError as e:
            self.assertEqual(self.pos.underlying_symbol, test_symbol)
            self.assertEqual(len(self.pos.transactions), 1)


    def test_long_buy_sell_transactions(self):
        txns = []

        test_symbol = 'SWKS'
        test_position_length = 30
        test_close_date = date.today()
        test_open_date = test_close_date - timedelta(days=test_position_length)
        txn = self.new_buy_transaction(test_price=95.25, test_date = test_open_date)
        txns.append(txn)

        txn = Transaction()
        txn = self.new_sell_transaction(test_price=99.25, test_date = test_close_date)
        txns.append(txn)

        test_total = 0.0
        for txn in txns:
            test_total = test_total + txn.amount

        self.pos.add_transactions(txns)
        self.assertEqual(self.pos.open_date, test_open_date)
        self.assertEqual(self.pos.close_date, test_close_date)
        self.assertEqual(self.pos.position_length, test_position_length + 1)
        self.assertEqual(self.pos.amount, test_total)


    def test_option_transaction(self):
        return