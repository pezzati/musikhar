
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from loginapp.serializers import UserProfileSerializer
from loginapp.forms import ProfileForm
from musikhar.abstractions.messages import ErrorMessaging
from musikhar.abstractions.views import IgnoreCsrfAPIView


class ProfileView(IgnoreCsrfAPIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        data = request.data
        form = ProfileForm(data)
        if form.is_valid():
            user = request.user
            serializer = UserProfileSerializer(instance=user)
            serializer.update(instance=user, validated_data=form.cleaned_data)
            return Response(data=serializer.data)

        errors = ErrorMessaging()
        errors = errors.get_errors(error_list=form.error_translator())
        return Response(data=errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        serializer = UserProfileSerializer(instance=request.user)
        data = serializer.data
        return Response(data=data, status=status.HTTP_200_OK)
