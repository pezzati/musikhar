from django.conf.urls import url, include

from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns

from analytics.views import LikeViewSet,FavoriteViewSet


router = routers.DefaultRouter()
router.register(r'like', LikeViewSet, 'get-like')
router.register(r'favorite', FavoriteViewSet, 'get-favorite')

