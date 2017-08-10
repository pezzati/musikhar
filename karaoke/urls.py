
from rest_framework import routers

from karaoke.views import GetKaraokeSerializer

router = routers.DefaultRouter()
router.register(r'karaoke', GetKaraokeSerializer,'get_karaoke')

urlpatterns = [

]


