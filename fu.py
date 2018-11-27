import csv
import Transaction


DATE = 0
ACTION = 1
SYMBOL = 2
DESCRIPTION = 3
FUNDS_TYPE = 4
QUANTITY = 5
PRICE = 6
COMMISSION = 7
FEES = 8
INTEREST = 9
AMOUNT = 10
SETTLEMENT_DATE = 11


def parse_row(map, web_format, row):

    # run date,action,symbol,security description,security type,quantity,price ($),commission ($),fees ($),accrued interest ($),amount ($),settlement date
    txn = Transaction.Transaction()

    txn.symbol = row[map['Symbol']]
    txn.description = row[map['Security Description']]
    txn.shares = row[map['Quantity']]
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


    #txn.date = row[DATE]
    #txn.action = row[ACTION]
    #txn.symbol = row[SYMBOL]
    #position = map['Symbol']
    #test = row[position]
    #txn.symbol = row['Symbol' in map]
    #txn.price = row[PRICE]
    #txn.quantity = row[QUANTITY]
    #txn.amount = row[AMOUNT]
    #txn.commission = row[COMMISSION]
    #txn.fees = row[FEES]
    #txn.funds_type = row[FUNDS_TYPE]


    print (txn)
    return txn


def import_csv(file_name):
    with open(file_name, newline='', encoding='utf-8') as f:
        reader = csv.reader(f)

        # Run Date,Action,Symbol,Security Description,Security Type,Quantity,Price ($),Commission ($),Fees ($),Accrued Interest ($),Amount ($),Settlement Date
        header_read = False
        for row in reader:
            print (row)
            if len(row) >= 12:
                if header_read:
                    txn = parse_row(map, web_format, row)
                else:
                    map = {field: position for position, field in enumerate(row) }
                    web_format = 'Run Date' in map
                    header_read = True

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