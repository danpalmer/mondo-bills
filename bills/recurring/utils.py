import strict_rfc3339

from django.utils import timezone

from bills.wizardry import detect_recurring_payments


def refresh_recurring_transactions(account):
    last_3_months = account.transactions.filter(
        mondo_created__gte=timezone.now(),
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
