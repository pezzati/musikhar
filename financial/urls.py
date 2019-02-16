from django.conf.urls import url

from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns

from financial.views import BusinessPackagesViewSet, Purchase, Bazzar, GiftCodeViewSet

router = routers.DefaultRouter()
router.register(r'packages', BusinessPackagesViewSet, base_name='get-song')
router.register(r'giftcodes', GiftCodeViewSet, base_name='gift-code')

urlpatterns = [
    url(r'^purchase$', Purchase.as_view(), name='purchase'),
    url(r'^bazzar_paymnet', Bazzar.as_view(), name='bazzar_payment')
]

urlpatterns = format_suffix_patterns(urlpatterns) + router.urls
