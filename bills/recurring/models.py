from dateutil import relativedelta

from django.db import models
from django.utils import timezone


class RecurringTransaction(models.Model):
    account = models.ForeignKey(
        'accounts.Account',
        related_name='recurring_transactions',
    )

    merchant_group = models.ForeignKey(
        'transactions.MerchantGroup',
        related_name='recurring_transactions',
    )

    predicted_day_of_month = models.IntegerField()
    predicted_amount = models.IntegerField()

    def formatted_amount(self):
        amount_pounds = -float(self.predicted_amount) / 100.0
        return '£%.2f' % amount_pounds

    def formatted_day_of_month(self):
        now = timezone.now()
        due = now.replace(day=self.predicted_day_of_month)

        if due < now:
            due += relativedelta.relativedelta(months=1)

        return due.strftime('%b %-d')

    def paid_this_month(self):
        now = timezone.now()
        return self.predicted_day_of_month < now.day
