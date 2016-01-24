from django.utils.timesince import timeuntil
from django.contrib.staticfiles.storage import staticfiles_storage

from bills import mondo
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

    if account.nearing_zero_balance():
        mondo.insert_feed_item(
            account.user,
            account.mondo_account_id,
            {
                'title': "Top up your account in the next %s to avoid running out of money" % (
                    timeuntil(account.time_of_zero_balance)
                ),
                'image_url': staticfiles_storage.url(
                    'images/money-with-wings.png',
                ),
            },
        )
