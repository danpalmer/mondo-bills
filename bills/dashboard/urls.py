from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^dashboard$', views.Dashboard.as_view(), name='view'),
]
