from django.views.generic import ListView

from bills.recurring.models import RecurringTransaction


class Dashboard(ListView):
    template_name = 'dashboard/view.html'
    context_object_name = 'recurring_transactions'

    def get_queryset(self):
        return RecurringTransaction.objects.filter(
            account__user=self.request.user,
        )
