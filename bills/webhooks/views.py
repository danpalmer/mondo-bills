from django.http import HttpResponse
from django.views.generic import DetailView
from django.db.transaction import on_commit

from bills.accounts.models import Account

class Hook(DetailView):
    model = Account

    def post(self, request, pk):
        account = self.get_object()
        # TODO: receive the webhook
        return HttpResponse()
