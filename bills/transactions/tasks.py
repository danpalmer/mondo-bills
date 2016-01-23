from dateutil import parser as dateparser
from django.contrib.auth import get_user_model

from bills.celery import queue
from bills.accounts.models import Account
from bills.transactions.models import MerchantGroup
from bills import mondo

def download_all_transactions(account):
    receive_transaction_hook_task.delay(account.pk)

@queue.task
def download_all_transactions_task(account_id):
    account = Account.objects.get(pk=account_id)
    user = account.user

    transactions = mondo.get_all_transactions(user, account.mondo_account_id)

    for data in transactions:
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
