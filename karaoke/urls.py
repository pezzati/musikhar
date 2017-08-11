
from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns

from karaoke.views import GetKaraokeSerializer

router = routers.DefaultRouter()
router.register(r'karaoke', GetKaraokeSerializer,'get_karaoke')

urlpatterns = [

]

urlpatterns = format_suffix_patterns(urlpatterns) + router.urls


