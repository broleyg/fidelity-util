from unittest import TestCase
from datetime import date
from Position import Position

class TestPosition(TestCase):
    def setUp(self):
        self.pos = Position()

class TestInit(TestPosition):

    def test_initial_symbol(self):
        self.assertEqual(self.pos.symbol, "")

    def test_initial_description(self):
        self.assertEqual(self.pos.description, "")

    def test_initial_quantity(self):
        self.assertEqual(self.pos.quantity, 0)


class TestQuantity(TestPosition):
    def setUp(self):
        self.pos = Position()

    def test_valid_quantity(self):
        test_quantity = 12.01
        self.pos.quantity = test_quantity
        self.assertEqual(self.pos.quantity, test_quantity)

    def test_invalid_quantity(self):
        test_quantity = '-12x.01'
        try:
            self.pos.quantity = test_quantity
            self.failIfEqual(self.pos.quantity, test_quantity)
        except ValueError as e:
            self.assertEqual(self.pos.quantity, 0)


class TestIsOption(TestCase):
    def setUp(self):
        self.pos = Position()

    def test_no_symbol(self):
        self.pos.symbol = None
        self.assertFalse(self.pos.is_option)

    def test_regular_pos(self):
        test_symbol = 'SWKS'
        self.pos.symbol = test_symbol
        self.assertFalse(self.pos.is_option)

    def test_option_pos(self):
        test_symbol = "-SWKS180119P105"
        self.pos.symbol = test_symbol
        self.assertTrue(self.pos.is_option)


class TestSymbol(TestCase):
    def setUp(self):
        self.pos = Position()

    def test_no_symbol(self):
        self.pos.symbol = None
        self.assertFalse(self.pos.symbol, "")

    def test_regular_pos(self):
        test_symbol = 'SWKS'
        self.pos.symbol = test_symbol
        self.assertEqual(self.pos.symbol, test_symbol)
        self.assertFalse(self.pos.is_option)

    def test_option_pos(self):
        test_symbol = "-SWKS180119P105.50"
        self.pos.symbol = test_symbol
        self.assertEqual(self.pos.symbol, 'SWKS')
        self.assertTrue(self.pos.is_option)
        self.assertEqual(self.pos.option_symbol, test_symbol[1:])
        self.assertEqual(self.pos.option_type, Position.PUT)
        self.assertEqual(self.pos.option_expiration_date, date(2018, 1, 19))
        self.assertEqual(self.pos.option_strike_price, 105.50)

    def test_bad_option_expiration_date(self):
        test_symbol = "-SWKS180132P105.50"
        try:
            self.pos.symbol = test_symbol
            self.fail("An invalid expiration day should have thrown a ValueError")
        except AttributeError as e:
            self.assertTrue(True, e)

    def test_bad_option_type(self):
        test_symbol = "-SWKS180119X105.50"
        try:
            self.pos.symbol = test_symbol
            self.fail("An invalid option type (e.g. CALL/BUY) should have thrown a ValueError")
        except AttributeError as e:
            self.assertTrue(True, e)

    def test_bad_option_strike_price(self):
        test_symbol = "-SWKS180119Px105.50"
        try:
            self.pos.symbol = test_symbol
            self.fail("An invalid expiration price should have thrown a ValueError, not {}".format(self.pos.option_strike_price))
        except AttributeError as e:
            self.assertTrue(True, e)

    def test_no_option_strike_price(self):
        test_symbol = "-SWKS180119Px"
        try:
            self.pos.symbol = test_symbol
            self.fail("An invalid expiration price should have thrown a ValueError")
        except AttributeError as e:
            self.assertTrue(True, e)

    def test_no_option_symbol(self):
        test_symbol = "-180119P105.50"
        try:
            self.pos.symbol = test_symbol
            self.fail("An invalid underlying stock symbol should have thrown a ValueError")
        except AttributeError as e:
            self.assertTrue(True, e)
