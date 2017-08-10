from django.conf.urls import url

from loginapp.views.edit_profile_views import ProfileView
from loginapp.views.login_views import DeviceSignUpView, UserSignup

urlpatterns = [
    url(r'^profile$', ProfileView.as_view(), name='user_profile'),
    url(r'^device_signup$', DeviceSignUpView.as_view(), name='device_signup_profile'),
    url(r'^login$', UserSignup.as_view(), name='login')
]
