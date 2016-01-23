#!/usr/bin/env python
# -*- encoding:utf-8 -*-

"""
Reads in a bunch of transactions, detects recurring payments, defined as:
    RULE 1. Same merchant group_id.
    RULE 2. Occurs in 2+ consecutive months.
    RULE 3. Exclude transaction category 'eating_out'
    RULE 4. Exclude months containing 3+ transactions.
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


# Helper functions

def longest_run(data):
    """Return length of longest run of consectuive integers in a list"""
    return max([len(map(itemgetter(1), g)) for k, g in groupby(enumerate(data), lambda (i, x): i - x)])


def get_merchant_data(k):
    """Get shit out of merchant dict"""
    return [row[k] if (row is not None and k in row) else '' for row in df['merchant']]


# Read in transactions JSON data
with open('sample_transactions_expanded.json') as f:
    transactions = json.loads(f.read())

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
            matching_merchants += [(merchant, merchant_name)]

# Examine results
# pprint(matching_merchants)

# Examine individual merchant
# df[df['merchant_group_id'] == 'grp_000094LTtN8eei7muPEvUv']
