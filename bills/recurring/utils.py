import strict_rfc3339

from django.utils import timezone

from bills.wizardry import detect_recurring_payments


def refresh_recurring_transactions(account):
    last_3_months = account.transactions.filter(
        mondo_created__gte=timezone.now(),
    )

    recurring_merchants = get_recurring_merchants(last_3_months)

def get_recurring_merchants(transactions):
    transactions = transactions.filter(merchant_group__isnull=False)

    dictified_txs = []
    for tx in transactions:
        merchant = tx.merchant_group
        dictified_txs.append({
            'amount': tx.amount,
            'category': tx.category,
            'created': strict_rfc3339.timestamp_to_rfc3339_utcoffset(
                tx.mondo_created.timestamp(),
            ),
            'merchant': {
                'id': merchant.mondo_group_id,
                'group_id': merchant.mondo_group_id,
                'name': merchant.name,
            },
        })

    return detect_recurring_payments.process_transactions({
        'transactions': dictified_txs
    })
