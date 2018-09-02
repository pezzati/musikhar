from django.conf.urls import url, include

from rest_framework.urlpatterns import format_suffix_patterns

from mediafiles.views import UploadMediaFile, UploadWebhook, DeleteWebhook

webhook_urls = [
    url(r'^upload', UploadWebhook.as_view(), name='upload'),
    url(r'^delete', DeleteWebhook.as_view(), name='delete')
]

urlpatterns = [
    url(r'^upload/(?P<type>[a-z]*)$', UploadMediaFile.as_view(), name='password_recovery'),
    url(r'^webhook/', include(webhook_urls, namespace='webhooks'))
]

urlpatterns = format_suffix_patterns(urlpatterns)

