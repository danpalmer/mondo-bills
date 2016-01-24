from dateutil import parser as dateparser
import strict_rfc3339

from bills.transactions.models import MerchantGroup
from bills.wizardry import detect_recurring_payments


def store_transaction(account, data):
    merchant = None
    if data['merchant']:
        merchant, _ = MerchantGroup.objects.get_or_create(
            mondo_group_id=data['merchant']['group_id'],
            defaults={
                'name': data['merchant']['name'],
                'logo_url': data['merchant']['logo'],
                'category': data['merchant']['category'],
            },
        )

    account.transactions.get_or_create(
        mondo_transaction_id=data['id'],
        defaults={
            'description': data['description'],
            'amount': data['amount'],
            'is_load': data['is_load'],
            'category': data['category'],
            'mondo_created': dateparser.parse(data['created']),
            'merchant_group': merchant,
        },
    )


def get_recurring_merchants(account):
    txs = account.transactions.all().select_related('merchant_group')
    dictified_txs = []
    for tx in txs:
        merchant = tx.merchant_group
        dictified_txs.append({
            'amount': tx.amount,
            'category': tx.category,
            'created': strict_rfc3339.timestamp_to_rfc3339_utcoffset(
                tx.mondo_created.timestamp(),
            ),
            'merchant': {
                'id': getattr(merchant, 'mondo_group_id', 'NA'),
                'group_id': getattr(merchant, 'mondo_group_id', 'NA'),
                'name': getattr(merchant, 'name', 'NA'),
            },
        })

    return detect_recurring_payments.process_transactions({
        'transactions': dictified_txs
    })
