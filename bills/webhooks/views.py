import json

from django.http import HttpResponse
from django.views.generic import DetailView
from django.db.transaction import on_commit

from bills.accounts.models import Account

from .tasks import receive_transaction_hook

class Hook(DetailView):
    model = Account

    def post(self, request, pk):
        account = self.get_object()

        tx_json = json.loads(request.body.decode('utf8'))
        on_commit(lambda: receive_transaction_hook(account, tx_json))

        return HttpResponse()
