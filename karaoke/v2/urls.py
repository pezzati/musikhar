
from django.conf.urls import url
from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns

from karaoke.v2.homefeed import HomeFeedV2
from karaoke.viewsets import SongViewSet, GenreViewSet, PoemViewSet, PostViewSet, KaraokeViewSet, FeedViewSet

router = routers.DefaultRouter()
router.register(r'songs', SongViewSet, base_name='get-song')
router.register(r'genre', GenreViewSet, 'get-genre')
router.register(r'poems', PoemViewSet, 'get-poem')
router.register(r'posts', PostViewSet, 'get-post')
router.register(r'karaokes', KaraokeViewSet, 'get-karaoke')
router.register(r'feeds', FeedViewSet, 'get-feed')

urlpatterns = [
    url(r'^home$', HomeFeedV2.as_view(), name='home'),
]

urlpatterns = format_suffix_patterns(urlpatterns) + router.urls


