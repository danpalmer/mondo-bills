from django.db import models
from django.contrib.auth.models import User

from bills.core.fields import OneToOneField


class MondoUser(models.Model):
    user = OneToOneField(User, related_name='mondo_user')

    mondo_user_id = models.CharField(max_length=50, unique=True)
    access_token = models.CharField(max_length=512, unique=True)
    access_expires = models.DateTimeField()
    refresh_token = models.CharField(max_length=512, unique=True)


class Account(models.Model):
    user = models.ForeignKey(User, related_name='accounts')
    description = models.CharField(max_length=100)
    webhook_id = models.CharField(max_length=50, unique=True)
    mondo_account_id = models.CharField(max_length=50, unique=True)

    current_balance = models.IntegerField(default=0)

    def __str__(self):
        return self.description

    def formatted_balance(self):
        amount_pounds = float(self.current_balance) / 100.0
        return '£%.2f' % amount_pounds

    def formatted_outgoings(self):
        total = self.recurring_transactions.aggregate(
            sum=models.Sum('predicted_amount'),
        )['sum']

        amount_pounds = -float(total) / 100.0

        return '£%.2f' % amount_pounds
