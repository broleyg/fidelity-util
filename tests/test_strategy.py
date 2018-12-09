from unittest import TestCase

from datetime import date
from Strategy import Strategy

class TestStrategy(TestCase):
    def setUp(self):
        self.strat = Strategy()

class TestCoveredCallStrategy(TestStrategy):

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
        self.pos.update()
        self.assertEqual(self.pos.open_date, test_open_date)
        self.assertEqual(self.pos.close_date, test_close_date)
        self.assertEqual(self.pos.position_length, test_position_length)
        self.assertEqual(self.pos.amount, test_total)