
from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns

from karaoke.viewsets import SongViewSet, GenreViewSet, PoemViewSet, PostViewSet

router = routers.DefaultRouter()
router.register(r'songs', SongViewSet, base_name='get-song')
router.register(r'genre', GenreViewSet, 'get-genre')
router.register(r'poems', PoemViewSet, 'get-poem')
router.register(r'posts', PostViewSet, 'get-post')

urlpatterns = [

]

urlpatterns = format_suffix_patterns(urlpatterns) + router.urls


