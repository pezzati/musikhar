from django.conf.urls import url, include

from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns

from loginapp.views.edit_profile_views import ProfileView, FollowingViewSet, UploadProfilePicture
from loginapp.views.login_views import UserSignup, PasswordRecovery, Verify, SignupGoogle, NassabLogin, NassabCallBack
from loginapp.viewsets import ArtistViewSet, UserViewSet

router = routers.DefaultRouter()
router.register(r'artists', ArtistViewSet, 'get-artist')
router.register(r'follow', FollowingViewSet, 'follow-relations')
router.register(r'users', UserViewSet, 'get-user')

profile_urls = [
    url(r'^upload_pic', UploadProfilePicture.as_view(), name='upload_profile_picture'),
    url(r'^verify', Verify.as_view(), name='verify_user'),
    url(r'^$', ProfileView.as_view(), name='user_profile'),
]


urlpatterns = [
    url(r'^profile/', include(profile_urls, namespace='profile')),
    url(r'^signup$', UserSignup.as_view(), name='signup'),
    url(r'^google_signup$', SignupGoogle.as_view(), name='signup_google'),
    # url(r'^login$', UserLogin.as_view(), name='login'),
    url(r'^recovery', PasswordRecovery.as_view(), name='password_recovery'),
    url(r'^gettoken', NassabLogin.as_view(), name='nassablogin'),
    url(r'^nassabcallback', NassabCallBack.as_view(), name='nassabcallback'),
]

urlpatterns = format_suffix_patterns(urlpatterns) + router.urls

