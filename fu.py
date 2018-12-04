import csv
from Security import Security
from Transaction import Transaction

from Account import Account

def parse_row(map, web_format, row):

    # run date,action,symbol,security description,security type,quantity,price ($),commission ($),fees ($),accrued interest ($),amount ($),settlement date
    txn = Transaction()

    txn.symbol = row[map['Symbol']].strip()
    txn.description = row[map['Security Description']].strip()
    txn.quantity = row[map['Quantity']].strip()
    txn.settlement_date = row[map['Settlement Date']].strip()
    if web_format:
        txn.date = row[map['Run Date']].strip()
        txn.action = row[map['Action']].strip()
        txn.funds_type = row[map['Security Type']].strip()
        txn.price = row[map['Price ($)']].strip()
        txn.commission = row[map['Commission ($)']].strip()
        txn.fees = row[map['Fees ($)']].strip()
        txn.amount = row[map['Amount ($)']].strip()
    else:
        txn.date = row[map['Date']].strip()
        txn.action = row[map['Description']].strip()
        txn.funds_type = row[map['Type']].strip()
        txn.price = row[map['Price']].strip()
        txn.commission = row[map['Commission']].strip()
        txn.fees = row[map['Fees']].strip()
        txn.amount = row[map['Amount']].strip()
    #txn.interest = row[map['Accrued Interest ($)']]
    #print (txn)
    return txn


def import_csv(file_name):
    txns = []
    with open(file_name, newline='', encoding='utf-8') as f:
        reader = csv.reader(f)

        # Run Date,Action,Symbol,Security Description,Security Type,Quantity,Price ($),Commission ($),Fees ($),Accrued Interest ($),Amount ($),Settlement Date
        header_read = False
        for row in reader:
            #print (row)
            if len(row) >= 12:
                if header_read:
                    txn = parse_row(map, web_format, row)
                    if (txn.symbol != ''):
                        txns.append(txn)
                else:
                    map = {field: position for position, field in enumerate(row) }
                    web_format = 'Run Date' in map
                    header_read = True
    return txns


def convert_line(line):
    return

def export_json(conten):
    return

def main():
    act = Account()

    #act = import_csv('data/example-transactions.csv')
    txns = import_csv('data/2014-roth-txns.csv')
    act.add_transactions(txns)
    txns = import_csv('data/2015-roth-txns.csv')
    act.add_transactions(txns)
    txns = import_csv('data/2016-roth-txns.csv')
    act.add_transactions(txns)
    txns = import_csv('data/2017-roth-txns.csv')
    act.add_transactions(txns)
    txns = import_csv('data/2018-roth-txns.csv')
    act.add_transactions(txns)

    for symbol, position in act.positions.items():
        print()
        print('{} transactions from {} to {} ({}) day(s)'.format(symbol, position.open_date, position.close_date, position.position_length))
        print()
        for txn in position.transactions:
            print('{0}  {1:<18} {2:<15} {3:>6} {4:>12} {5:>6} {6:>6} {7:>15}'.format(txn.date, txn.symbol, txn.action, txn.quantity, Security.currency_format(txn.price), Security.currency_format(txn.commission), Security.currency_format(txn.fees), Security.currency_format(txn.amount)))
        print('{0}'.format('-'*80))
        print('{0:62}{1:>15}'.format(' ', Security.currency_format(position.amount)))
    return

if (__name__ == "__main__"):
    main();