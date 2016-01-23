from django.shortcuts import redirect
from django.utils.crypto import get_random_string
from django.views.generic.base import View
from django.views.generic.edit import BaseFormView
from django.core.urlresolvers import reverse

from bills import mondo

from .forms import LoginReceiveForm, OAUTH_STATE_KEY
from .utils import refresh_accounts


class LoginRedirect(View):
    def get(self, request):
        state = get_random_string()
        request.session[OAUTH_STATE_KEY] = state

        redirect_uri = reverse('accounts:login-receive')

        return redirect(mondo.auth_redirect(state, redirect_uri))


class LoginReceive(BaseFormView):
    form_class = LoginReceiveForm

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.get = self.post

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()

        kwargs.update({
            'request': self.request,
            'data': self.request.GET,
        })

        return kwargs

    def form_invalid(self, form):
        import ipdb; ipdb.set_trace()
        return redirect('home:view')

    def form_valid(self, form):
        form.save(self.request)
        refresh_accounts(self.request.user)
        return redirect('dashboard:view')
