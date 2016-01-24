from django.views.generic import TemplateView

from bills.transactions import utils


class Dashboard(TemplateView):
    template_name = 'dashboard/view.html'


    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(self, *args, **kwargs)
        to_return = {}
        to_return.update(ctx)
        user = self.request.user

        accounts = []
        for account in self.user.accounts.all():
            accounts.append({
                'actual_account': account,
                'recurring_transactions': utils.get_recurring_merchants(account),
            })
        to_return.update({
            'user': self.request.user,
            'accounts': accounts,
        })

        return to_return
