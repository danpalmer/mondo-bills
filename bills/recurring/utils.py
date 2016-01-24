import itertools
import datetime
import strict_rfc3339

from dateutil import relativedelta
from django.utils import timezone

from bills.wizardry import detect_recurring_payments
from bills.transactions.models import MerchantGroup

from .models import RecurringTransaction


def refresh_recurring_transactions(account):
    last_3_months = account.transactions.filter(
        mondo_created__gte=timezone.now() - datetime.timedelta(days=100),
    )

    recurring_merchants = get_recurring_merchants(last_3_months)

    for recurring_merchant in recurring_merchants:
        merchant_group = MerchantGroup.objects.filter(
            mondo_group_id=recurring_merchant['group_id'],
        ).first()

        day_of_month = recurring_merchant['predicted_next_day_of_month']
        amount = recurring_merchant['predicted_next_amount']

        RecurringTransaction.objects.get_or_create(
            account=account,
            merchant_group=merchant_group,
            defaults={
                'predicted_day_of_month': day_of_month,
                'predicted_amount': amount,
            }
        )

def get_recurring_merchants(transactions):
    transactions = transactions.filter(merchant_group__isnull=False)
    if not transactions:
        return []

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


def time_of_zero_balance(account):
    now = timezone.now()
    current_balance = account.current_balance

    r_txs = RecurringTransaction.objects.filter(
        account=account,
    ).order_by(
        'predicted_day_of_month',
    )

    for month, payment in generate_payments(r_txs):
        current_balance += payment.predicted_amount
        if current_balance <= 0:
            break

    return now + relativedelta.relativedelta(
        months=month,
        day=payment.predicted_day_of_month,
    )


def generate_payments(r_txs):
    count = itertools.count()
    month = next(count)
    for transaction in r_txs:
        if not transaction.paid_this_month():
            yield month, transaction

    for month in count:
        for transaction in r_txs:
            yield month, transaction
