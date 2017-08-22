from django.conf.urls import url
from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns

from loginapp.views.edit_profile_views import ProfileView
from loginapp.views.login_views import UserSignup, UserLogin
from loginapp.viewsets import ArtistViewSet

router = routers.DefaultRouter()
router.register(r'artists', ArtistViewSet, base_name='get_artist')

urlpatterns = [
    url(r'^profile$', ProfileView.as_view(), name='user_profile'),
    url(r'^signup$', UserSignup.as_view(), name='signup'),
    url(r'^login$', UserLogin.as_view(), name='login')
]

urlpatterns = format_suffix_patterns(urlpatterns) + router.urls

