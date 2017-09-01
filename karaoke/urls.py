
from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns

from karaoke.viewsets import KaraokeViewSet, GenreViewSet

router = routers.DefaultRouter()
router.register(r'karaoke', KaraokeViewSet, base_name='get-karaoke')
router.register(r'genre', GenreViewSet, 'get-genre')

urlpatterns = [

]

urlpatterns = format_suffix_patterns(urlpatterns) + router.urls


