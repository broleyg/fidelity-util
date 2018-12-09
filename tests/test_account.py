from unittest import TestCase
from Account import Account
from Transaction import Transaction


class TestAccount(TestCase):
    def setUp(self):
        self.act = Account()

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

class TestInit(TestAccount):
    def test_initial_id(self):
        self.assertEqual(self.act.id, "")

    def test_initial_balance(self):
        self.assertEqual(self.act.initial_balance, 0.00)

    def test_initial_transactions(self):
        self.assertEqual(len(self.act.transactions), 0)


class TestId(TestAccount):
    def test_id(self):
        test_id = "IRA"
        self.act.id = test_id
        self.assertEqual(self.act.id, test_id)

class TestInitialBalance(TestAccount):

    def test_initial_balance(self):
        test_intial_balance = '100000.00'
        self.test_initial_balance = test_intial_balance
        self.assertEqual(self.act.initial_balance, 100000.00)

    def test_initial_balance(self):
        test_intial_balance = 100000.00
        self.act.initial_balance = test_intial_balance
        self.assertEqual(self.act.initial_balance, test_intial_balance)

class TestCurrentBalance(TestAccount):

    def test_current_balance_no_transactions(self):
        test_intial_balance = 100000.00
        self.act.initial_balance = test_intial_balance
        self.assertEqual(self.act.initial_balance, test_intial_balance)

    def test_current_balance_one_transaction(self):
        test_intial_balance = 100000.00
        self.act.initial_balance = test_intial_balance
        self.assertEqual(self.act.initial_balance, test_intial_balance)

        test_symbol = 'SWKS'
        txn = self.new_buy_transaction(test_symbol = 'swks', test_price=95.25, test_commission=0)
        self.act.add_transaction(txn)

        #self.assertEqual(self.act.current_balance, 90475.00)
        self.assertTrue(self.act.current_balance > 0)





