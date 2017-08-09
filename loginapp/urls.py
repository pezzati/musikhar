from django.conf.urls import url, include
from django.contrib import admin

from loginapp.views.edit_profile_views import ProfileView
from loginapp.views.login_views import test_view

urlpatterns = [
    url(r'profile$', ProfileView.as_view(), name='user_profile'),
]
