from bills.celery import queue
from bills.accounts.models import Account
from bills import mondo

from . import utils

def download_all_transactions(account):
    download_all_transactions_task.delay(account.pk)

@queue.task
def download_all_transactions_task(account_id):
    account = Account.objects.get(pk=account_id)
    user = account.user

    transactions = mondo.get_all_transactions(user, account.mondo_account_id)

    for data in transactions:
        utils.store_transaction(account, data)
