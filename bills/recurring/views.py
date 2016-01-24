from django.shortcuts import get_object_or_404, redirect
from django.views.generic import View

from .models import RecurringTransaction


class IgnoreView(View):
    def post(self, request, recurring_transaction_id, **kwargs):
        transaction = get_object_or_404(
            RecurringTransaction.objects.filter(
                account__user=request.user,
            ),
            pk=recurring_transaction_id,
        )

        transaction.is_subscription = False
        transaction.save()

        return redirect('dashboard:view')
