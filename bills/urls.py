from django.conf import settings
from django.contrib import admin
from django.conf.urls import include, url
from django.conf.urls.static import static

urlpatterns = [

    url(r'^admin/', include(admin.site.urls)),

    url(r'', include('bills.home.urls', namespace='home')),
    url(r'^account/', include('bills.accounts.urls', namespace='accounts')),
    url(r'^webhook/', include('bills.webhooks.urls', namespace='webhooks')),
    url(r'^', include('bills.dashboard.urls', namespace='dashboard')),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )
