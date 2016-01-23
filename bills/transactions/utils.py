from dateutil import parser as dateparser

from bills.transactions.models import MerchantGroup


def store_transaction(account, transaction):
    data = transaction
    merchant = None
    if data['merchant']:
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
