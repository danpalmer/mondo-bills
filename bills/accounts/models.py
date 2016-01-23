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

    current_balance = models.IntegerField()

    def __str__(self):
        return self.description
