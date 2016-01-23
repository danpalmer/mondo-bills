from django.db import models


class Transaction(models.Model):
    amount = models.IntegerField()
    decline_reason = models.CharField(max_length=100, null=True)
    is_load = models.BooleanField(default=False)
    category = models.CharField(max_length=100)
