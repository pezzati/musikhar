
from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns

from karaoke.views import KaraokeViewSet, GenreViewSet

router = routers.DefaultRouter()
router.register(r'karaoke', KaraokeViewSet, 'get_karaoke')
router.register(r'genre', GenreViewSet, 'get_genre')

urlpatterns = [

]

urlpatterns = format_suffix_patterns(urlpatterns) + router.urls


