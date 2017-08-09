from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from loginapp.forms import SignupForm
from musikhar.abstractions.views import IgnoreCsrfAPIView
from loginapp.models import Token
from rest_framework import status


class Signup(IgnoreCsrfAPIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        data = request.data
        form = SignupForm(data)
        user = request.user
        if form.is_valid():
           user.username = form.cleaned_data.get('username')
           user.mobile = form.cleaned_data.get('moblie')
           token = Token.objects.create(user=user)

           user.save()

           return Response(data={'token': token.key},status=status.HTTP_200_OK)
