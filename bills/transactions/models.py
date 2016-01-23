from django.db import models


class MerchantGroup(models.Model):
    name = models.CharField(max_length=100)
    logo_url = models.URLField()
    category = models.CharField(max_length=100)
    mondo_group_id = models.CharField(max_length=100, unique=True)


class Transaction(models.Model):
    account = models.ForeignKey(
        'accounts.Account',
        related_name='transactions',
    )

    mondo_transaction_id = models.CharField(max_length=100, unique=True)

    description = models.CharField(max_length=512)

    amount = models.IntegerField()
    is_load = models.BooleanField(default=False)
    category = models.CharField(max_length=100)
    merchant_group = models.ForeignKey(
        MerchantGroup,
        null=True,
        related_name='transactions',
    )

    mondo_created = models.DateTimeField()
