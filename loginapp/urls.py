from django.conf.urls import url

from loginapp.views.edit_profile_views import ProfileView
from loginapp.views.login_views import UserSignup, UserLogin, PasswordRecovery

urlpatterns = [
    url(r'^profile$', ProfileView.as_view(), name='user_profile'),
    url(r'^signup$', UserSignup.as_view(), name='signup'),
    url(r'^login$', UserLogin.as_view(), name='login'),
    url(r'^recovery', PasswordRecovery.as_view(), name='password_recovery')
]
