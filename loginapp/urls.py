from django.conf.urls import url, include

from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns

from loginapp.views.edit_profile_views import ProfileView, FollowingViewSet
from loginapp.views.login_views import UserSignup, UserLogin, PasswordRecovery
from loginapp.viewsets import ArtistViewSet

router = routers.DefaultRouter()
router.register(r'artists', ArtistViewSet, 'get-artist')
router.register(r'follow', FollowingViewSet, 'follow-relations')

profile_urls = [
    url(r'^$', ProfileView.as_view(), name='user_profile'),
]


urlpatterns = [
    url(r'^profile/', include(profile_urls, namespace='profile')),
    url(r'^signup$', UserSignup.as_view(), name='signup'),
    url(r'^login$', UserLogin.as_view(), name='login'),
    url(r'^recovery', PasswordRecovery.as_view(), name='password_recovery')
]

urlpatterns = format_suffix_patterns(urlpatterns) + router.urls

