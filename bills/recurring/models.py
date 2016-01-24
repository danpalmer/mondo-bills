from django.db import models


class RecurringTransaction(models.Model):
    account = models.ForeignKey(
        'accounts.Account',
        related_name='recurring_transactions',
    )

    merchant = models.ForeignKey(
        'transactions.MerchantGroup',
        related_name='recurring_transactions',
    )

    predicted_day_of_month = models.IntegerField()
    predicted_amount = models.IntegerField()
