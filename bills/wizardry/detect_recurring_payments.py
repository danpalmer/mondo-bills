#!/usr/bin/env python

# -*- encoding:utf-8 -*-

"""
Reads in a bunch of transactions, detects recurring payments, defined as:
    RULE 1. Same merchant group_id.
    RULE 2. Occurs in 2+ consecutive months.
    RULE 3. Exclude transaction category 'eating_out'
    RULE 4. Exclude months containing 3+ transactions.

Predicts date & amount of next recurring expense:
    DATE: Most common, or most recent
    COST: Average spend.
"""

from dateutil import relativedelta as rdel, parser
from datetime import datetime
from itertools import groupby
import json
from operator import itemgetter
import pandas as pd


# Config stuff that could be functionalised
CONSECUTIVE_MONTHS = 2
MAX_TRANSACTIONS_PER_MONTH = 2


def process_transactions(txs):

    # Helper functions

    def longest_run(data):
        """Return length of longest run of consectuive integers in a list"""
        def do_a_thing(wtf):
            i, x = wtf
            return i - x
        grouped = groupby(enumerate(data), do_a_thing)
        return max(
            len(list(map(itemgetter(1), g))) for k, g in grouped
        )


    def get_merchant_data(k):
        """Get shit out of merchant dict"""
        return [row[k] if (row is not None and k in row) else '' for row in df['merchant']]

    transactions = txs


    df = pd.DataFrame(transactions['transactions'])
    df['merchant_id'] = get_merchant_data('id')
    df['merchant_name'] = get_merchant_data('name')
    df['merchant_group_id'] = get_merchant_data('group_id')

    # Add %Y-%m col
    df['year_month'] = pd.Series([datetime.strftime(parser.parse(x), '%Y-%m-01') for x in df['created']])

    # RULE 3. Exclude transaction category 'eating_out'
    df = df[df['category'] != 'eating_out']

    # RULE 1. Same merchant group_id (get list of all merchants (merchant_group_id)
    merchants = df[df['merchant_group_id'] != '']['merchant_group_id'].unique()  # ignore blanks
    matching_merchants = []

    for merchant in merchants:
        merchant_transactions = df[df['merchant_group_id'] == merchant].sort(['created'])
        transactions_by_month = merchant_transactions['year_month'].value_counts().reset_index().sort(['index'])
        # RULE 4. Exclude months containing 3+ transactions.
        if max(transactions_by_month['year_month']) <= MAX_TRANSACTIONS_PER_MONTH:
            months_since_1970 = [rdel.relativedelta(parser.parse(x), parser.parse('1970-01-01'))
                                 for x in transactions_by_month['index']]
            absolute_months = [(12 * x.years + x.months) for x in months_since_1970]
            # RULE 2. Occurs in 2+ consecutive months.
            if longest_run(absolute_months) >= CONSECUTIVE_MONTHS:
                merchant_name = merchant_transactions['merchant_name'].unique()[0]
                # Calculate predicted date
                days_of_month = pd.Series(parser.parse(x).day for x in merchant_transactions['created'])
                date_counts = days_of_month.value_counts()
                if len(date_counts[date_counts == max(date_counts)]) == 1:
                    predicted_date = date_counts[date_counts == max(date_counts)].index[0]
                else:  # go with most recent
                    predicted_date = list(days_of_month)[-1]
                # Calculate predicted value (avg)
                predicted_amount = int(merchant_transactions['amount'].mean())
                # Write out
                matching_merchants += [{'group_id': merchant,
                                        'name': merchant_name,
                                        'predicted_next_day_of_month': predicted_date,
                                        'predicted_next_amount': predicted_amount}]

    return matching_merchants

# Examine results
# pprint(matching_merchants)

# Examine individual merchant
# df[df['merchant_group_id'] == 'grp_000094LTtN8eei7muPEvUv']
