"""musikhar URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

from mediafiles.views import get_file, webhook, Webhook
from musikhar.views import Handshake, home

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^user/', include('loginapp.urls', namespace='users')),
    url(r'^song/', include('karaoke.urls', namespace='songs')),
    url(r'^analysis/', include('analytics.urls', namespace='analysis')),
    url(r'^media-management/', include('mediafiles.urls', namespace='mediafiles')),
    url(r'^finance/', include('financial.urls', namespace='finance')),

    url(r'^handshake$', Handshake.as_view(), name='handshake'),
    url(r'^uploads/', get_file, name='get_file'),
    url(r'^silk/', include('silk.urls', namespace='silk')),
    url(r'^webhook', Webhook.as_view(), name='webhook'),
    url(r'^$', home, name='home')
] #+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
