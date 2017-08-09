import json

from django.utils.decorators import method_decorator
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from loginapp.serializers import UserProfileSerializer
from loginapp.auth import if_authorized
from loginapp.forms import ProfileForm


class ProfileView(APIView):

    @method_decorator(if_authorized)
    def dispatch(self, request, *args, **kwargs):
        return super(ProfileView, self).dispatch(request=request, *args, **kwargs)

    def post(self, request):
        data = json.loads(request.body)
        form = ProfileForm(data)
        if form.is_valid():
            user = request.user
            # TODO update users info

    def get(self, request):
        serializer = UserProfileSerializer(instance=request.user)
        data = serializer.data
        return Response(data=data, status=status.HTTP_200_OK)
