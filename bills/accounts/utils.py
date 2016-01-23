from django.db.transaction import on_commit

from bills import mondo

from .tasks import install_webhook
from bills.transactions.tasks import download_all_transactions


def refresh_accounts(user):
    accounts = mondo.get_accounts(user)
    for account in accounts['accounts']:
        account, created = user.accounts.update_or_create(
            mondo_account_id=account['id'],
            defaults={
                'description': account['description'],
            },
        )

        if created or account.current_balance == 0:
            balance = mondo.get_balance(user, account)
            account.current_balance = balance['balance']
            account.save()

        download_all_transactions(account)

        if not account.webhook_id:
            on_commit(lambda: install_webhook(account))
