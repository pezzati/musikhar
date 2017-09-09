from django.conf.urls import url

from rest_framework.urlpatterns import format_suffix_patterns

from mediafiles.views import UploadMediaFile

urlpatterns = [
    url(r'^upload/(?P<type>[a-z]*)$', UploadMediaFile.as_view(), name='password_recovery')
]

urlpatterns = format_suffix_patterns(urlpatterns)

