from unittest import TestCase
from datetime import date
from datetime import timedelta
from Position import Position
from Transaction import Transaction

class TestPosition(TestCase):
    def setUp(self):
        self.pos = Position()

    def new_txn(self,test_symbol='', test_action='', test_date='', test_quantity='', test_price='', test_commission='', test_fees='', test_amount=''):
        txn = Transaction()
        txn.symbol = test_symbol
        txn.action = test_action
        txn.quantity= test_quantity
        txn.commission = test_commission
        txn.fees = test_fees
        txn.price = test_price
        txn.date = test_date
        txn.amount = test_amount
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
        txn = self.new_txn(test_symbol = 'swks', test_price=95.25)
        self.pos.add_transaction(txn)

        txn = self.new_txn(test_symbol = 'APPL', test_price=99.25)

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
        txn = self.new_txn(test_symbol, test_action=Transaction.BUY, test_price=95.25, test_date = test_open_date)
        txns.append(txn)

        txn = Transaction()
        txn = self.new_txn(test_symbol, test_action=Transaction.SELL, test_price=99.25, test_date = test_close_date)
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

class TestCoveredCallPosition(TestPosition):
    def test_covered_call(self):
        txns = []

        test_symbol = 'SQ'
        test_open_date = date(2018, 6, 25)
        test_close_date = date(2018, 11, 22)
        test_close_date = date.today()

        test_position_length = (test_close_date - test_open_date).days + 1

        #txn = self.new_txn('-SQ180817P50', Transaction.SELL, '2018-05-23', -1, 2.55, 5.60, .05, 249.35)
        #txns.append(txn)
        #txn = self.new_txn('-SQ180817P50', Transaction.EXPIRED, '2018-08-20', 1, 0, 0, 0, 0)
        #txns.append(txn)

        txn = self.new_txn('SQ', Transaction.BUY, '06/25/2018', 200, 63.0, 4.95, 0, -12604.95)
        txns.append(txn)
        txn = self.new_txn('-SQ180817C65', Transaction.SELL, '06/25/2018', -2, 3.78, 1.30, .09, 754.61)
        txns.append(txn)
        txn = self.new_txn('-SQ180817C65', Transaction.BUY, '08/15/2018', 2, 7.42, 1.30, .07, -1485.37)
        txns.append(txn)
        txn = self.new_txn('-SQ181221C70', Transaction.SELL, '08/15/2018', -2, 9.17, 6.25, .10, 1827.65)
        txns.append(txn)
        txn = self.new_txn('-SQ181221C70', Transaction.BUY, '11/22/2018', 2, 6.22, 6.25, 0.07, -1250.32)
        txns.append(txn)
        txn = self.new_txn('-SQ190118C75', Transaction.SELL, '11/22/2018', -2, 5.27, 1.30, .09, 1052.61)
        txns.append(txn)


        test_total = 0.0
        for txn in txns:
            test_total = test_total + txn.amount

        #self.pos.add_transactions(txns)
        self.pos.transactions = txns
        self.pos.update_position()
        self.assertEqual(self.pos.open_date, test_open_date)
        self.assertEqual(self.pos.close_date, test_close_date)
        self.assertEqual(self.pos.position_length, test_position_length)
        self.assertEqual(self.pos.amount, test_total)