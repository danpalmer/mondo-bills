from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from . import views


urlpatterns = [
    url(
        r'^recurring/(?P<recurring_transaction_id>\d+)/ignore$',
        login_required(views.IgnoreView.as_view()),
        name='ignore',
    ),
]
