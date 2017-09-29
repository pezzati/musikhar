from django.conf.urls import url, include

from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns

from analytics.views import LikeViewSet, FavoriteViewSet, TagViewSet

router = routers.DefaultRouter()
router.register(r'like', LikeViewSet, 'get-like')
router.register(r'favorite', FavoriteViewSet, 'get-favorite')
router.register(r'tag', TagViewSet, 'get-tags')

urlpatterns = [

]

urlpatterns = format_suffix_patterns(urlpatterns) + router.urls