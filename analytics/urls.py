from django.conf.urls import url, include

from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns

from analytics.views import TagViewSet, BannerViewSet, NotificationViewSet, UserActionViewSet

router = routers.DefaultRouter()
# router.register(r'like', LikeViewSet, 'get-like')
# router.register(r'favorite', FavoriteViewSet, 'get-favorite')
router.register(r'tag', TagViewSet, 'get-tags')
router.register(r'banners', BannerViewSet, 'get-banners')
router.register(r'notifs', NotificationViewSet, 'get-notifs')
router.register(r'actions', UserActionViewSet, 'user-actions')

urlpatterns = [

]

urlpatterns = format_suffix_patterns(urlpatterns) + router.urls
