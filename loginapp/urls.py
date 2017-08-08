from django.conf.urls import url, include
from django.contrib import admin

from loginapp.views.login_views import test_view

urlpatterns = [
    url(r'^test$', test_view)
]
