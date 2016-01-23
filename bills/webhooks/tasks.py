from dateutil import parser as dateparser

from bills.celery import queue
from bills.accounts.models import Account
from bills.transactions.models import MerchantGroup

def receive_transaction_hook(account, transaction):
    receive_transaction_hook_task.delay(account.pk, transaction)

@queue.task
def receive_transaction_hook_task(account_id, transaction):
    account = Account.objects.get(pk=account_id)

    if transaction['type'] != 'transaction.created':
        return

    data = transaction['data']

    merchant, _ = MerchantGroup.objects.get_or_create(
        mondo_group_id=data['merchant']['group_id'],
        defaults={
            'name': data['merchant']['name'],
            'logo_url': data['merchant']['logo'],
            'category': data['merchant']['category'],
        },
    )

    account.transactions.create(
        mondo_transaction_id=data['id'],
        description=data['description'],
        amount=data['amount'],
        is_load=data['is_load'],
        category=data['category'],
        mondo_created=dateparser.parse(data['created']),
        merchant_group=merchant,
    )
