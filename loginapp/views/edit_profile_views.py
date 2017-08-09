import json

from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authentication import BasicAuthentication
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from loginapp.auth import CsrfExemptSessionAuthentication
from loginapp.serializers import UserProfileSerializer
from loginapp.forms import ProfileForm


class ProfileView(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    def post(self, request):
        data = request.data
        form = ProfileForm(data)
        if form.is_valid():
            user = request.user
            serializer = UserProfileSerializer(instance=user)
            serializer.update(instance=user, validated_data=form.cleaned_data)
            return Response(data=serializer.data)
        print(form.errors)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        serializer = UserProfileSerializer(instance=request.user)
        data = serializer.data
        return Response(data=data, status=status.HTTP_200_OK)
