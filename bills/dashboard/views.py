import itertools

from django.views.generic import TemplateView

from bills.recurring.models import RecurringTransaction
from bills.recurring.utils import refresh_recurring_transactions


class Dashboard(TemplateView):
    template_name = 'dashboard/view.html'
    context_object_name = 'recurring_transactions'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        transactions = RecurringTransaction.objects.filter(
            account__user=self.request.user,
        ).order_by(
            'predicted_day_of_month',
        ).select_related(
            'account',
            'merchant_group',
        )

        context['account_transactions'] = itertools.groupby(
            transactions,
            lambda x: x.account,
        )

        return context

    def get(self, *args, **kwargs):
        refresh_recurring_transactions(self.request.user.accounts.first())
        return super().get(*args, **kwargs)
