import json
import re
import datetime
import locale

class Position:

    CALL = 'C'
    PUT ='P'

    locale.setlocale(locale.LC_ALL, '')
    __conv = locale.localeconv()

    def __init__(self):
        self.symbol = ""
        self.__underlying_symbol = ""
        self.description = ""
        self.__quantity = 0
        self.__is_option = False
        self.__option_type = None
        self.__option_symbol = ""
        self.__option_strike_price = 0.00
        self.__option_expiration_date = ""

    def __str__(self):
        rep = {}
        for key, value in self.__dict__.items():
            pos = key.rfind('__')
            if pos > 0:
                attr = key[pos+2:]
            else:
                attr = key
            rep[attr] = value
        return json.dumps(rep, indent=4, sort_keys=True, default=str)

    def __currency_value(self, value):
        if isinstance(value, str):
            no_currency = value.replace(self.__conv['currency_symbol'], '')
            raw_numbers = no_currency.replace(self.__conv['thousands_sep'], '')
            return raw_numbers
        else:
            return value

    def __date_value(self, value):
        if isinstance(value, str) and (value.strip() != ''):
            format = locale.nl_langinfo(locale.D_FMT)
            date_value = datetime.datetime.strptime(value.strip(), format).date()
            return date_value
        elif isinstance(value, datetime.date):
            return value
        else:
            return None

    @property
    def quantity(self):
        return self.__quantity

    @quantity.setter
    def quantity(self, new_quantity):
        try:
            value = float(self.__currency_value(new_quantity))
        except ValueError as e:
            if new_quantity == '':
                value = 0.00
            else:
                raise ValueError("Inavlid shares {}".format(new_quantity))

        self.__quantity = value

    @property
    def symbol(self):
       return self.__symbol

    @symbol.setter
    def symbol(self, new_symbol):

        # First, ensure that we have a value provided, to avoid all the costly regular expression searching
        if new_symbol is None:
           self.__symbol = ''
           self.__option_symbol = ''
           self.__underlying_symbol = ''
           self.__is_option = False

        # .. so now that we know have a value ...
        else:

            # Lets check and see if it's an option symbol, which has the following format
            #
            #  -SWKS180132P105.50
            match = re.search("(?P<option_flag>\-?)(?P<symbol>[A-Z]*)(?P<exp_year>\d{2})(?P<exp_mon>\d{2})(?P<exp_day>\d{2})(?P<opt_type>[A-Z])(?P<strike_price>\d*\.?\d*)", new_symbol)

            if match:

                self.__is_option = (match.group('option_flag') == '-')
                self.__option_symbol = new_symbol

                underlying_symbol = match.group('symbol')
                if underlying_symbol == '':
                    raise AttributeError('The underlying symbol was not found in the option symbol')
                else:
                    self.__symbol = new_symbol[1:]
                    self.__underlying_symbol = underlying_symbol


                exp_yr = int('20' + match.group('exp_year'))
                exp_mo = int(match.group('exp_mon'))
                exp_day = int(match.group('exp_day'))
                try:
                    #exp_date = datetime.date(exp_yr, exp_mo, exp_day)
                    str_date = '{}/{}/20{}'.format(match.group('exp_mon'), match.group('exp_day'), match.group('exp_year'))
                    exp_date = self.__date_value(str_date)
                except ValueError as e:
                    raise AttributeError("Invalid expiration date: {}".format(e))
                self.__option_expiration_date = exp_date

                opt_type = match.group('opt_type')
                if (opt_type == Position.CALL) or (opt_type == Position.PUT):
                    self.__option_type = opt_type
                else:
                    raise AttributeError("An option type must be a 'C' (CALL) or a 'P' (PUT)")

                price = match.group('strike_price')
                if price == '':
                    raise AttributeError("Invalid or missing option price {}".format(price))
                else:
                    self.__option_strike_price = float(price)

            else:

                if new_symbol[0:1] == '-':
                    raise AttributeError('Invalid option symbol {}'.format(new_symbol))

                else:
                    self.__symbol = new_symbol
                    self.__option_symbol = ''
                    self.__underlying_symbol = new_symbol
                    self.__is_option = False


    @property
    def is_option(self):
        return self.__is_option

    @is_option.setter
    def is_option(self, option):
        raise ValueError("is_option flag is read only")

    @property
    def option_type(self):
        return self.__option_type

    @property
    def option_symbol(self):
        return self.__option_symbol

    @property
    def option_expiration_date(self):
        return self.__option_expiration_date

    @property
    def option_strike_price(self):
        return self.__option_strike_price

    @property
    def underlying_symbol(self):
        return self.__underlying_symbol