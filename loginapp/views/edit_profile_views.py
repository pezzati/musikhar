
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from loginapp.serializers import UserProfileSerializer
from loginapp.forms import ProfileForm
from musikhar.abstractions.messages import ErrorMessaging
from musikhar.abstractions.views import IgnoreCsrfAPIView
from musikhar.utils import Errors, get_not_none


class ProfileView(IgnoreCsrfAPIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        data = request.data
        form = ProfileForm(data)
        if form.is_valid():
            user = request.user
            serializer = UserProfileSerializer(instance=user)
            user = serializer.update(instance=user, validated_data=form.cleaned_data)
            if get_not_none(form.cleaned_data, 'password'):
                user.set_password(raw_password=form.cleaned_data.get('password'))
            return Response(data=serializer.data)

        errors = Errors.get_errors(Errors, error_list=form.error_translator())
        return Response(data=errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        serializer = UserProfileSerializer(instance=request.user)
        data = serializer.data
        return Response(data=data, status=status.HTTP_200_OK)
