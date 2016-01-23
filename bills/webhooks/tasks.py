from bills import mondo
from bills.celery import queue
from bills.accounts.models import Account

def receive_transaction_hook(account, transaction):
    receive_transaction_hook_task.delay(account.pk, transaction)

@queue.task
def receive_transaction_hook_task(account_id, transaction):
    account = Account.objects.get(pk=account_id)

    print(transaction)
    print(account)
