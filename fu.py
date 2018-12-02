import csv
import Transaction

from Account import Account

def parse_row(map, web_format, row):

    # run date,action,symbol,security description,security type,quantity,price ($),commission ($),fees ($),accrued interest ($),amount ($),settlement date
    txn = Transaction.Transaction()

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

    for symbol in act.positions:
        print()
        print('{} transactions amounting to {}'.format(symbol, act.get_total_amount_for_symbol(symbol)))
        txns = act.get_transactions_for_symbol(symbol)
        for txn in txns:
            print('\t{0} - {1:<18} {2:,.2f} {3}'.format(txn.date, txn.symbol,  txn.amount, txn.action))

    return

if (__name__ == "__main__"):
    main();