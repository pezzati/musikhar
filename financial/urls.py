from django.conf.urls import url

from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns

from financial.views import BusinessPackagesViewSet, Purchase

router = routers.DefaultRouter()
router.register(r'packages', BusinessPackagesViewSet, base_name='get-song')

urlpatterns = [
    url(r'^purchase$', Purchase.as_view(), name='purchase'),
]

urlpatterns = format_suffix_patterns(urlpatterns) + router.urls
