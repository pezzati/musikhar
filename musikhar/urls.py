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

from mediafiles.views import get_file
from musikhar.v2.views import HandshakeV2
from musikhar.views import Handshake, home, Repeater, bazzar, privacy, get_last_android

urlpatterns = [
    url(r'^GHVkDzDDmk2W7FX0/', admin.site.urls),

    url(r'^user/', include('loginapp.urls', namespace='users')),

    url(r'^song/', include('karaoke.urls', namespace='songs')),
    url(r'^v2/song/', include('karaoke.v2.urls', namespace='v2_songs')),

    url(r'^analysis/', include('analytics.urls', namespace='analysis')),

    url(r'^media-management/', include('mediafiles.urls', namespace='mediafiles')),

    url(r'^finance/', include('financial.urls', namespace='finance')),

    url(r'^handshake$', Handshake.as_view(), name='handshake'),
    url(r'^v2/handshake$', HandshakeV2.as_view(), name='v2_handshake'),

    url(r'^repeater/$', Repeater.as_view(), name='repeater'),

    url(r'^uploads/', get_file, name='get_file'),
    url(r'^bazzar', bazzar, name='bazzar'),
    # url(r'^silk/', include('silk.urls', namespace='silk')),
    # url(r'^webhook', UploadWebhook.as_view(), name='webhook'),
    url(r'^$', home, name='home'),
    url(r'^privacy', privacy, name='privacy'),
    url(r'^last-android$', get_last_android, name='last_android')
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
