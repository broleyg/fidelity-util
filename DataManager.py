import csv
from Transaction import Transaction

class DataManager():

    def __init__(self):
        self.transaction_files = {}

        self.transactions = []
        self.prices = {}

    def add_transaction_file(self, transact_file_name):
        if transact_file_name not in self.transaction_files:
            dataset = {"filename": transact_file_name, "field_map": {}, "transactions": []}
            self.transaction_files[transact_file_name] = dataset
            txns = self.import_transaction_csv(dataset['filename'])
            dataset['transactions']  = txns


    def parse_transaction_row(self, map, web_format, row):

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
        # txn.interest = row[map['Accrued Interest ($)']]
        # print (txn)
        return txn


    def import_transaction_csv(self,file_name):
        txns = []
        with open(file_name, newline='', encoding='utf-8') as f:
            reader = csv.reader(f)

            # Run Date,Action,Symbol,Security Description,Security Type,Quantity,Price ($),Commission ($),Fees ($),Accrued Interest ($),Amount ($),Settlement Date
            header_read = False
            for row in reader:
                # print (row)
                if len(row) >= 12:
                    if header_read:
                        txn = self.parse_transaction_row(map, web_format, row)
                        if (txn.symbol != ''):
                            txns.append(txn)
                    else:
                        map = {field: position for position, field in enumerate(row)}
                        web_format = 'Run Date' in map
                        self.transaction_files[file_name]["field_map"] = map
                        header_read = True
        self.transaction_files[file_name]['transactions'] = txns
        return txns

