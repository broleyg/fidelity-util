from unittest import TestCase

from datetime import date
from Transaction import Transaction
from Strategy import Strategy
from Security import Security

class TestStrategy(TestCase):
    def setUp(self):
        self.strat = Strategy()

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


class TestCoveredCallStrategy(TestStrategy):

    def test_covered_call(self):
        txns = []

        test_symbol = 'SQ'
        test_open_date = date(2018, 6, 25)
        test_close_date = date.today()

        test_stratition_length = (test_close_date - test_open_date).days + 1

        Security.price_list['SQ'] = 60.00
        Security.price_list['-SQ190118C75'] = 5

        #txn = self.new_txn('-SQ180817P50', Transaction.SELL, '2018-05-23', -1, 2.55, 5.60, .05, 249.35)
        #txns.append(txn)
        #txn = self.new_txn('-SQ180817P50', Transaction.EXPIRED, '2018-08-20', 1, 0, 0, 0, 0)
        #txns.append(txn)

        txn = self.new_txn('SQ', Transaction.BUY, '06/25/2018', 200, 63.0, 4.95, 0, -12000)
        txns.append(txn)
        txn = self.new_txn('-SQ180817C65', Transaction.SELL, '06/25/2018', -2, 3.78, 1.30, .09, 1000)
        txns.append(txn)
        txn = self.new_txn('-SQ180817C65', Transaction.BUY, '08/15/2018', 2, 7.42, 1.30, .07, -1000)
        txns.append(txn)
        txn = self.new_txn('-SQ181221C70', Transaction.SELL, '08/15/2018', -2, 9.17, 6.25, .10, 2000)
        txns.append(txn)
        txn = self.new_txn('-SQ181221C70', Transaction.BUY, '11/22/2018', 2, 6.22, 6.25, 0.07, -3000)
        txns.append(txn)
        txn = self.new_txn('-SQ190118C75', Transaction.SELL, '11/22/2018', -2, 5.27, 1.30, .09, 1000)
        txns.append(txn)


        self.strat.add_transactions(txns)
        self.strat.transactions = txns
        self.strat.update()
        #self.assertEqual(self.strat.open_date, test_open_date)
        #self.assertEqual(self.strat.open_date, test_open_date)
        #self.assertEqual(self.strat.close_date, test_close_date)
        #self.assertEqual(self.strat.position_length_length, test_stratition_length)
        self.assertEqual(self.strat.realized_gain, -12000)
        self.assertEqual(self.strat.unrealized_gain, 11000)
        self.assertEqual(self.strat.amount, -1000)