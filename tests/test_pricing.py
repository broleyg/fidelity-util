from unittest import TestCase
from Pricing import Pricing


class TestPricing(TestCase):
    def setUp(self):
        self.pricer = Pricing()

class TestLookupPrice(TestPricing):

    def test_none(self):
        test_symbol = None
        price = 0.00
        try:
            price = self.pricer.lookup_price(test_symbol)
            self.fail('A value of None for symbol should throw an exception')
        except ValueError as e:
            self.assertEqual(price, 0.00)

    def test_empty_string(self):
        test_symbol = ''
        price = 0.00
        try:
            price = self.pricer.lookup_price(test_symbol)
            self.fail('An empty string for symbol should throw an exception')
        except ValueError as e:
            self.assertEqual(price, 0.00)

    def test_bad_string(self):
        test_symbol = 'ywwepqweerhihj'
        price = 0.00
        try:
            price = self.pricer.lookup_price(test_symbol)
            self.fail('{} is not a valid symbol'.format(test_symbol))
        except ValueError as e:
            self.assertEqual(price, 0.00)

    def test_valid_string(self):
        test_symbol = 'AAPL'
        price = self.pricer.lookup_price(test_symbol)
        self.assertTrue(price > 0.00)
