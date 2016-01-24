from django.utils import timezone


def refresh_recurring_transactions(account):
    last_3_months = account.transactions.filter(
        mondo_created__gte=timezone.now(),
    )
