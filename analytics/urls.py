from django.conf.urls import url

from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns

from analytics.views import LikeViewSet, FavoriteViewSet


router = routers.DefaultRouter()


urlpatterns = [
    url(r'^like$', LikeViewSet.as_view(), name='like'),
    url(r'^favorite$', FavoriteViewSet.as_view(), name='favorite'),
]

urlpatterns = format_suffix_patterns(urlpatterns) + router.urls
