from unittest import TestCase
from Account import Account
from Transaction import Transaction


class TestAccount(TestCase):
    def setUp(self):
        self.act = Account()

    def new_transaction(self,test_symbol = 'SWKS', test_price=100.00, test_quantity=100, test_commission = 4.95, test_fees = 0):
        txn = Transaction()
        txn.symbol = test_symbol
        txn.quantity= test_quantity
        txn.action = Transaction.BUY
        txn.commission = test_quantity
        txn.fees = test_fees
        txn.price = test_price
        txn.amount = (-1 * test_price * test_quantity) - test_commission - test_fees
        return txn

    def new_buy_transaction(self,test_symbol = 'SWKS', test_price=100.00, test_quantity=100, test_commission = 4.95, test_fees = 0):
        txn = self.new_transaction(test_symbol, test_price, test_quantity, test_commission, test_fees)
        txn.action = Transaction.BUY
        txn.amount = (-1 *test_price * test_quantity) - test_commission - test_fees
        return txn

    def new_sell_transaction(self,test_symbol = 'SWKS', test_price=100.00, test_quantity=100, test_commission = 4.95, test_fees = 0):
        txn = self.new_transaction(test_symbol, test_price, test_quantity, test_commission, test_fees)
        txn.action = Transaction.SELL
        txn.amount = (1 *test_price * test_quantity) - test_commission - test_fees
        return txn

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

        self.act.add_transactions(txns)
        self.assertEqual(len(self.act.transactions), len(txns))
        self.assertEqual(len(self.act.positions), 1)
        self.assertTrue(test_symbol in self.act.positions, "{} is not found in the account positions".format(test_symbol))


    def test_long_buy_sell_transactions(self):
        txns = []

        test_symbol = 'SWKS'
        txn = self.new_buy_transaction(test_price=95.25)
        #txn.symbol = test_symbol
        #txn.quantity= 100
        #txn.action = Transaction.BUY
        #txn.commission = 5.95
        #txn.fees = 0.00
        #txn.price = 95.25
        #txn.amount = -9530.95
        txns.append(txn)

        txn = Transaction()
        txn = self.new_sell_transaction(test_price=99.25)
        #txn.symbol = test_symbol
        ##txn.quantity= 100
        #txn.action = Transaction.SELL
        #txn.commission = 5.95
        #txn.fees = 0.00
        #txn.price = 99.25
        #txn.amount = 9919.05
        txns.append(txn)

        test_total = 0.0
        for txn in txns:
            test_total = test_total + txn.amount

        self.act.add_transactions(txns)
        self.assertTrue(test_symbol in self.act.positions, "{} is not found in the account positions".format(test_symbol))
        pos = self.act.positions[test_symbol]
        self.assertFalse(pos.open)
        total = self.act.get_total_amount_for_symbol(test_symbol)
        self.assertEquals(total, test_total)


    def test_option_transaction(self):
        return
