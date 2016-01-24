from django.views.generic import ListView

from bills.recurring.models import RecurringTransaction
from bills.recurring.utils import refresh_recurring_transactions


class Dashboard(ListView):
    template_name = 'dashboard/view.html'
    context_object_name = 'recurring_transactions'

    def get_queryset(self):
        return RecurringTransaction.objects.filter(
            account__user=self.request.user,
        )

    def get(self, *args, **kwargs):
        refresh_recurring_transactions(self.request.user.accounts.first())
        return super().get(*args, **kwargs)
