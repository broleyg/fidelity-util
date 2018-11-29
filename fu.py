import csv
import Transaction

from Account import Account

def parse_row(map, web_format, row):

    # run date,action,symbol,security description,security type,quantity,price ($),commission ($),fees ($),accrued interest ($),amount ($),settlement date
    txn = Transaction.Transaction()

    txn.symbol = row[map['Symbol']]
    txn.description = row[map['Security Description']]
    txn.quantity = row[map['Quantity']]
    txn.settlement_date = row[map['Settlement Date']]
    if web_format:
        txn.date = row[map['Run Date']]
        txn.action = row[map['Action']]
        txn.funds_type = row[map['Security Type']]
        txn.price = row[map['Price ($)']]
        txn.commission = row[map['Commission ($)']]
        txn.fees = row[map['Fees ($)']]
        txn.amount = row[map['Amount ($)']]
    else:
        txn.date = row[map['Date']]
        txn.action = row[map['Description']]
        txn.funds_type = row[map['Type']]
        txn.price = row[map['Price']]
        txn.commission = row[map['Commission']]
        txn.fees = row[map['Fees']]
        txn.amount = row[map['Amount']]
    #txn.interest = row[map['Accrued Interest ($)']]
    #print (txn)
    return txn


def import_csv(file_name):
    act = Account()

    with open(file_name, newline='', encoding='utf-8') as f:
        reader = csv.reader(f)

        # Run Date,Action,Symbol,Security Description,Security Type,Quantity,Price ($),Commission ($),Fees ($),Accrued Interest ($),Amount ($),Settlement Date
        header_read = False
        for row in reader:
            #print (row)
            if len(row) >= 12:
                if header_read:
                    txn = parse_row(map, web_format, row)
                    act.add_transaction(txn)
                else:
                    map = {field: position for position, field in enumerate(row) }
                    web_format = 'Run Date' in map
                    header_read = True

        print (act)
    return

def convert_line(line):
    return

def export_json(conten):
    return

def main():
    import_csv('data/example-transactions.csv')
    #import_csv('data/2016-roth-txns.csv')
    return

if (__name__ == "__main__"):
    main();