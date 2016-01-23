from django.conf.urls import url
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required

from . import views

urlpatterns = [
    url(
        r'^login$',
        views.LoginRedirect.as_view(),
        name='login',
    ),
    url(
        r'^login-receive$',
        views.LoginReceive.as_view(),
        name='login-receive',
    ),
    url(
        r'^logout$',
        login_required(auth_views.logout),
        {'next_page': reverse_lazy('home:view')},
        name='logout',
    )
]
