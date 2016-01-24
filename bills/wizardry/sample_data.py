import csv
import sys
import random
import datetime

COLUMNS =  [
    'Bill_Amt',
    'Bill_Ccy',
    'Merch_Name_DE43',
    'Txn_Desc',
    'POS_Data_DE61',
    'MCC_Code',
    'Merch_ID_DE42',
    'POS_Data_DE22',
    'Txn_Type',
    'Proc_Code',
    'ActBal',
    'Avl_Bal',
    'Txn_GPS_Date',
    'Ignore_offset_days',
    'Settle_Amt',
    'Settle_Ccy',
    'Acquirer_ID_DE32',
    'Additional_Amt_DE54',
    'Amt_Tran_Fee_DE28',
    'Auth_Code_DE38',
    'BlkAmt',
    'Cust_Ref',
    'FX_Pad',
    'Fee_Fixed',
    'Fee_Rate',
    'MCC_Desc',
    'MCC_Pad',
    'Note',
    'POS_Termnl_DE41',
    'POS_Time_DE12',
    'Resp_Code_DE39',
    'Ret_Ref_No_DE37',
    'Status_Code',
    'Token',
    'Trans_Link',
    'Txn_Amt',
    'Txn_Ccy',
    'Txn_Ctry',
    'Txn_ID',
    'Txn_Stat_Code',
    'Txn_Time_DE07',
    'Additional_Data_DE48',
    'Authorised_by_GPS',
    'AVS_Result',
    'CU_Group',
    'InstCode',
    'MTID',
    'ProductID',
    'Record_Data_DE120',
    'SubBIN',
    'TLogIDOrg',
    'VL_Group',
]

START_DATE = datetime.datetime(2015, 1, 1)
END_DATE = datetime.datetime(2015, 12, 31)

NON_SUB_MERCHANTS = [
    "PIZZA EXPRESS",
    "M&S SIMPLY FOOD - ST PANCRAS ST",
    "PRUFROCK COFFEE LONDON",
    "TFL.GOV.UK/CP 1",
    "PRET A MANGER PRET A MANGER",
    "WH SMITH LONDON",
    "AMAZON.CO.UK",
    "BYRON HAMBURGERS COWCROSS ST 5",
    "ROYAL BANK 9APR",
    "FIRST CAPITAL CONN CITY THAMESLI",
    "OCADO RETAIL LIMIT 01707 228000",
]


writer = csv.writer(sys.stdout)
writer.writerow(COLUMNS)


def write_row(balance, month, day, merchant, amount):
    amount = 0 - (float(amount) / 100.0)
    balance = float(balance) / 100.0

    d = datetime.datetime(
        2015, 11, 14,
        random.randint(0, 23),
        random.randint(0, 59),
        random.randint(0, 59),
    ).strftime('%Y-%m-%d %H:%M:%S.%f')

    writer.writerow([
        '%.2f' % amount,
        '826',
        merchant,
        merchant,
        '0260000020000300826SW1V 1PZ  ',
        '5814',
        '123',
        '051',
        'P',
        '000000',
        '%.2f' % balance,
        '%.2f' % balance,
        d,
        '90',
        '%.2f' % amount,
        '826',
        '',
        '',
        '',
        '',
        '',
        '',
        '',
        '',
        '',
        '',
        '',
        '',
        '',
        '',
        '',
        '',
        '',
        '',
        '',
        '%.2f' % amount, # Txn_Amt
        '826', # Txn_Ccy
        '',
        '',
        '',
        '',
        '',
        '',
        '',
        '',
        '',
        '',
        '',
        '',
        '',
        '',
        '',
    ])


def random_date():
    diff = END_DATE - START_DATE
    rand_seconds = random.randint(0, diff.total_seconds())
    return START_DATE + datetime.timedelta(seconds=rand_seconds)


def generate_random():
    # Generate a NON-subscription charge
    merchant = random.choice(NON_SUB_MERCHANTS)
    amount = random.randint(100, 8000)
    date = random_date()
    return (date.month, date.day, merchant, amount)


def generate_subscription(merchant, weekly, variable_days, amount, variable_amount):
    day_of_week = random.randint(1, 6)
    day_of_month = random.randint(0, 28)

    def generate_iteration(month, day, _amount):
        if variable_amount:
            _amount = _amount + random.uniform(_amount * 0.9, _amount * 2.0)
        if variable_days:
            day = random.randint(day - 2, day + 2)
        return (month, day, merchant, _amount)

    transactions = []

    for day in range(int((END_DATE - START_DATE).days)):
        date = START_DATE + datetime.timedelta(day)

        if weekly and (date.weekday() == day_of_week):
            transactions.append(
                generate_iteration(date.month, date.day, amount),
            )
        else: # Monthly
            if date.day == day_of_month:
                transactions.append(
                    generate_iteration(date.month, date.day, amount),
                )

    return transactions


def main():
    transactions = []
    for _ in range(1000):
        transactions.append(generate_random())

    for subscription in (
        ("ABEL & COLE", True, False, 1052, True),
        ("SPOTIFY", False, False, 999, False),
        ("GYMBOX LTD", False, True, 4500, False),
        ("EXPERIAN", False, False, 1295, False),
        ("O2 RETAIL LTD", False, False, 2500, True),
        ("LAMBETH COUNCIL", False, False, 8200, False),
    ):
        transactions.extend(generate_subscription(*subscription))

    balance = sum(x for _, _, _, x in transactions)

    write_row(balance, START_DATE.month, START_DATE.day, "SALARY", -balance)

    for transaction in sorted(transactions):
        write_row(balance, *transaction)
        balance = balance - transaction[3]


if __name__ == '__main__':
    main()
