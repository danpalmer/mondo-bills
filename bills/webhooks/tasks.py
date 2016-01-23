from bills.celery import queue
from bills.accounts.models import Account
from bills.transactions import utils as transaction_utils

def receive_transaction_hook(account, transaction):
    receive_transaction_hook_task.delay(account.pk, transaction)

@queue.task
def receive_transaction_hook_task(account_id, transaction):
    account = Account.objects.get(pk=account_id)

    if transaction['type'] != 'transaction.created':
        return

    transaction_utils.store_transaction(account, transaction['data'])
