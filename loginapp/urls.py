from django.conf.urls import url

from loginapp.views.edit_profile_views import ProfileView

urlpatterns = [
    url(r'profile$', ProfileView.as_view(), name='user_profile'),
]
