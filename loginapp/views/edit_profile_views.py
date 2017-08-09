import json

from django.utils.decorators import method_decorator
from loginapp.serializers import User_Profile_Serializer
from rest_framework.renderers import JSONRenderer
from django.views.generic.base import View
from loginapp.auth import if_authorized
from loginapp.forms import ProfileForm


@if_authorized
def update_user_profile(request):
   ## if request.method == 'POST':
        data = json.loads(request.body)
        user = request.user

        if data.get('username'):
            user.username = data.get('username')

        if data.get('password'):
            user.set_password()

        if data.get('email'):
            user.email = data.get('email')

        if data.get('mobile'):
            user.mobile = data.get('mobile')

        if data.get('gender'):
            user.gender = data.get('gender')

        if data.get('age') :
            user.age = data.get('age')

        user.save()


class ProfileView(View):

    @method_decorator(if_authorized)
    def dispatch(self, request, *args, **kwargs):
        return super(ProfileView, self).dispatch(request=request, *args, **kwargs)

    def post(self, request):
        data = json.loads(request.body)
        form = ProfileForm(data)
        if form.is_valid():
            update_user_profile(request)

            # TODO update users info

    def get(self, request):
        serializers = User_Profile_Serializer(request.user)
        serializers.data
        json = JSONRenderer().render(serializers)

        return json
