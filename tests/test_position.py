from unittest import TestCase
from datetime import date
from datetime import timedelta
from Position import Position
from Transaction import Transaction

from Security import Security

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


# class TestAmount(TestPosition):
#
#     def test_valid_amount(self):
#         test_amount = 100
#         self.pos.amount = test_amount
#         self.assertEqual(self.pos.amount, test_amount)
#
#     def test_invalid_amount(self):
#         test_amount = "lx"
#         try:
#             self.pos.amount = test_amount
#             self.failIfEqual(self.pos.amount, test_amount)
#         except ValueError as e:
#             self.assertEqual(self.pos.amount, 0)

class TestBasis(TestPosition):
    def test_valid_basis(self):
        self.fail('implement me')

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


    def test_closed_transactions(self):
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
        self.pos.update()
        self.assertEqual(self.pos.open_date, test_open_date)
        self.assertEqual(self.pos.close_date, test_close_date)
        self.assertEqual(self.pos.position_length, test_position_length + 1)
        self.assertEqual(self.pos.amount, test_total)


    def test_open_position(self):
        txn = Transaction()

        txn.symbol = "SWKS"
        txn.quantity= 100

        txn.action = Transaction.BUY
        txn.commission = 5.95
        txn.fees = 0.00
        txn.price = 95.25
        txn.amount = -9519.05
        txn.date = "11/18/2018"
        txn.settlement_date = "11/19/2018"

        self.pos.add_transaction(txn)
        self.pos.update()
        current_price = Security.get_quote(txn.symbol)
        test_amount = txn.amount + current_price * txn.quantity
        self.assertEqual(self.pos.amount, test_amount)


    def test_multi_sale_txn_open_position(self):
        txns = []

        test_total = 0.0
        test_symbol = 'SWKS'
        test_current_price = 40

        Security.price_list[test_symbol] = test_current_price
        test_position_length = 30
        test_close_date = date.today()
        test_open_date = test_close_date - timedelta(days=test_position_length)
        txn = self.new_txn(test_symbol, test_action=Transaction.BUY, test_amount=-3800, test_date = test_open_date, test_quantity=100)
        txns.append(txn)
        test_total = test_total + txn.amount

        txn = Transaction()
        txn = self.new_txn(test_symbol, test_action=Transaction.SELL, test_amount=2000, test_date = test_close_date, test_quantity=-50)
        txns.append(txn)
        test_total = test_total + txn.amount

        test_realized_gain = test_total
        test_unrealized_gain = 50 * test_current_price
        test_total = test_total + test_unrealized_gain


        self.pos.add_transactions(txns)
        self.pos.update()
        self.assertEqual(self.pos.open_date, test_open_date)
        self.assertEqual(self.pos.close_date, test_close_date)
        self.assertEqual(self.pos.position_length, test_position_length + 1)
        self.assertEqual(self.pos.amount, test_total)
        self.assertEqual(self.pos.realized_gain, test_realized_gain)
        self.assertEqual(self.pos.unrealized_gain, test_unrealized_gain)

    def test_multi_sale_txn_open_position(self):
        txns = []

        test_total = 0.0
        test_symbol = 'SWKS190118C95'
        test_current_price = 2.00

        Security.price_list['-'+test_symbol] = test_current_price
        test_position_length = 30
        test_close_date = date.today()
        test_open_date = test_close_date - timedelta(days=test_position_length)
        txn = self.new_txn(test_symbol, test_action=Transaction.BUY, test_amount=-380, test_date = test_open_date, test_quantity=2)
        txns.append(txn)
        test_total = test_total + txn.amount

        txn = Transaction()
        txn = self.new_txn(test_symbol, test_action=Transaction.SELL, test_amount=200, test_date = test_close_date, test_quantity=-1)
        txns.append(txn)
        test_total = test_total + txn.amount

        test_realized_gain = test_total
        test_unrealized_gain = 1 * 100 * test_current_price
        test_total = test_total + test_unrealized_gain


        self.pos.add_transactions(txns)
        self.pos.update()
        self.assertEqual(self.pos.open_date, test_open_date)
        self.assertEqual(self.pos.close_date, test_close_date)
        self.assertEqual(self.pos.position_length, test_position_length + 1)
        self.assertEqual(self.pos.amount, test_total)
        self.assertEqual(self.pos.realized_gain, test_realized_gain)
        self.assertEqual(self.pos.unrealized_gain, test_unrealized_gain)

    def test_complex_open_position(self):
        txns = []

        test_total = 0.0
        test_symbol = 'SWKS'
        test_current_price = 40

        Security.price_list[test_symbol] = test_current_price
        test_position_length = 30
        test_close_date = date.today()
        test_open_date = test_close_date - timedelta(days=test_position_length)
        txn = self.new_txn(test_symbol, test_action=Transaction.BUY, test_amount=-3800, test_date=test_open_date,
                           test_quantity=100)
        txns.append(txn)
        test_total = test_total + txn.amount

        txn = Transaction()
        txn = self.new_txn(test_symbol, test_action=Transaction.SELL, test_amount=2000, test_date=test_close_date, test_quantity=-50)
        txns.append(txn)
        test_total = test_total + txn.amount

        txn = Transaction()
        txn = self.new_txn(test_symbol, test_action=Transaction.SELL, test_amount=2000, test_date=test_close_date, test_quantity=-40)
        txns.append(txn)
        test_total = test_total + txn.amount

        txn = Transaction()
        txn = self.new_txn(test_symbol, test_action=Transaction.SELL, test_amount=2000, test_date=test_close_date, test_quantity=-1)
        txns.append(txn)
        test_total = test_total + txn.amount



        test_total = test_total + 9 * test_current_price

        self.pos.add_transactions(txns)
        self.pos.update()
        self.assertEqual(self.pos.open_date, test_open_date)
        self.assertEqual(self.pos.close_date, test_close_date)
        self.assertEqual(self.pos.position_length, test_position_length + 1)
        self.assertEqual(self.pos.amount, test_total)

    def test_complex_closed_position(self):
        txns = []

        test_total = 0.0
        test_symbol = 'SWKS'
        test_current_price = 40

        Security.price_list[test_symbol] = test_current_price
        test_position_length = 30
        test_close_date = date.today()
        test_open_date = test_close_date - timedelta(days=test_position_length)
        txn = self.new_txn(test_symbol, test_action=Transaction.BUY, test_amount=-3800, test_date=test_open_date, test_quantity=30)
        txns.append(txn)
        test_total = test_total + txn.amount

        txn = self.new_txn(test_symbol, test_action=Transaction.BUY, test_amount=-3800, test_date=test_open_date, test_quantity=70)
        txns.append(txn)
        test_total = test_total + txn.amount

        txn = Transaction()
        txn = self.new_txn(test_symbol, test_action=Transaction.SELL, test_amount=2000, test_date=test_close_date, test_quantity=-50)
        txns.append(txn)
        test_total = test_total + txn.amount

        txn = Transaction()
        txn = self.new_txn(test_symbol, test_action=Transaction.SELL, test_amount=2000, test_date=test_close_date, test_quantity=-40)
        txns.append(txn)
        test_total = test_total + txn.amount

        txn = Transaction()
        txn = self.new_txn(test_symbol, test_action=Transaction.SELL, test_amount=2000, test_date=test_close_date, test_quantity=-10)
        txns.append(txn)
        test_total = test_total + txn.amount


        self.pos.add_transactions(txns)
        self.pos.update()
        self.assertEqual(self.pos.open_date, test_open_date)
        self.assertEqual(self.pos.close_date, test_close_date)
        self.assertEqual(self.pos.position_length, test_position_length + 1)
        self.assertEqual(self.pos.amount, test_total)

    def test_multi_close_option_position(self):
        txns = []

        test_total = 0.0
        test_symbol = 'NILE160219P35'
        test_current_price = 2.00

        #Security.price_list['-'+test_symbol] = test_current_price
        test_position_length = 30
        test_close_date = date.today()
        test_open_date = test_close_date - timedelta(days=test_position_length)
        txn = self.new_txn(test_symbol, test_action=Transaction.BUY, test_amount=-380, test_date = test_open_date, test_quantity=2)
        txns.append(txn)
        test_total = test_total + txn.amount

        txn = Transaction()
        txn = self.new_txn(test_symbol, test_action=Transaction.SELL, test_amount=200, test_date = test_close_date, test_quantity=-1)
        txns.append(txn)
        test_total = test_total + txn.amount

        txn = Transaction()
        txn = self.new_txn(test_symbol, test_action=Transaction.SELL, test_amount=200, test_date = test_close_date, test_quantity=-1)
        txns.append(txn)
        test_total = test_total + txn.amount

        test_realized_gain = test_total
        test_unrealized_gain = 0


        self.pos.add_transactions(txns)
        self.pos.update()
        self.assertEqual(self.pos.open_date, test_open_date)
        self.assertEqual(self.pos.close_date, test_close_date)
        self.assertEqual(self.pos.position_length, test_position_length + 1)
        self.assertEqual(self.pos.amount, test_total)
        self.assertEqual(self.pos.realized_gain, test_realized_gain)
        self.assertEqual(self.pos.unrealized_gain, test_unrealized_gain)

    def test_multi_invalid_option_position(self):
        txns = []

        test_total = 0.0
        test_symbol = 'NILE160219P35'
        test_current_price = 2.00

        # Security.price_list['-'+test_symbol] = test_current_price
        test_position_length = 30
        test_close_date = date.today()
        test_open_date = test_close_date - timedelta(days=test_position_length)
        txn = self.new_txn(test_symbol, test_action=Transaction.BUY, test_amount=-380, test_date=test_open_date,
                           test_quantity=2)
        txns.append(txn)
        test_total = test_total + txn.amount

        txn = Transaction()
        txn = self.new_txn(test_symbol, test_action=Transaction.SELL, test_amount=200, test_date=test_close_date,
                           test_quantity=-1)
        txns.append(txn)
        test_total = test_total + txn.amount

        txns.append(txn)
        test_total = test_total + txn.amount

        test_realized_gain = test_total
        test_unrealized_gain = 1 * 100 * test_current_price
        test_total = test_total + test_unrealized_gain

        try:
            self.pos.add_transactions(txns)
            self.pos.update()
            self.fail('Unbalances transactions for an expired option contract should have thrown an exception')
        except ValueError as e:
            self.assertTrue(True)

    def test_hal_fix_test(self):
        # HAL transactions from 2015-06-26 to 2018-12-08 (1262) day(s)
        #
        # 2015-06-26 HAL                BUY                    115.0       $42.98  $7.95  $0.00         $-4,951.14
        # 2015-09-23 HAL                DIVIDEND                 0.0        $0.00  $0.00  $0.00             $20.70
        # 2015-12-24 HAL                DIVIDEND                 0.0        $0.00  $0.00  $0.00             $20.70
        # 2016-03-23 HAL                DIVIDEND                 0.0        $0.00  $0.00  $0.00             $20.70
        # 2016-06-22 HAL                DIVIDEND                 0.0        $0.00  $0.00  $0.00             $20.70
        # 2016-08-17 HAL                SELL                  -115.0       $44.50  $7.95  $0.12          $5,109.43
        # ---------------------------------------------------------------------------------------------------------
        # $7,067.49
        txns = []

        test_total = 0.0
        test_symbol = 'HAL'

        test_position_length = 30
        test_close_date = date.today()
        test_open_date = test_close_date - timedelta(days=test_position_length)

        txn = self.new_txn(test_symbol, test_action=Transaction.BUY, test_amount=-4951.14, test_date='06/26/2015', test_quantity=115)
        txns.append(txn)
        test_total = test_total + txn.amount

        txn = self.new_txn(test_symbol, test_action=Transaction.DIVIDEND, test_amount=20.70, test_date='09/23/2015', test_quantity=0)
        txns.append(txn)
        test_total = test_total + txn.amount

        txn = self.new_txn(test_symbol, test_action=Transaction.DIVIDEND, test_amount=20.70, test_date='12/24/2015', test_quantity=0)
        txns.append(txn)
        test_total = test_total + txn.amount

        txn = self.new_txn(test_symbol, test_action=Transaction.DIVIDEND, test_amount=20.70, test_date='03/23/2016', test_quantity=0)
        txns.append(txn)
        test_total = test_total + txn.amount

        txn = self.new_txn(test_symbol, test_action=Transaction.DIVIDEND, test_amount=20.70, test_date='06/22/2016', test_quantity=0)
        txns.append(txn)
        test_total = test_total + txn.amount

        txn = Transaction()
        txn = self.new_txn(test_symbol, test_action=Transaction.SELL, test_amount=5109.43, test_date='08/17/2016', test_quantity=-115)
        txns.append(txn)
        test_total = test_total + txn.amount


        self.pos.add_transactions(txns)
        self.pos.update()
        self.assertTrue(test_total, self.pos.amount)

