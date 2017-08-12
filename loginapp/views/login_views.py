from django.db.utils import IntegrityError
from rest_framework.response import Response
from rest_framework import status
from loginapp.models import User, Token
from musikhar.abstractions.views import IgnoreCsrfAPIView
from loginapp.forms import SignupForm, LoginForm


class UserSignup(IgnoreCsrfAPIView):

    def post(self, request):
        if request.user.is_authenticated():
            return Response(data={'token': request.user.token_set.first().key})

        data = request.data
        form = SignupForm(data)
        if form.is_valid():

            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            try:
                user = User.objects.create(username=username)
                user.set_password(raw_password=password)
            except IntegrityError:
                # TODO error msg already signed up
                return Response(status=status.HTTP_400_BAD_REQUEST)

            user.country = form.cleaned_data.get('country')
            user.save()

            token = Token.objects.create(user=user)
            return Response(data={'token': token.key}, status=status.HTTP_200_OK)

        print(form.errors)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class UserLogin(IgnoreCsrfAPIView):

    def post(self, request):
        data = request.data
        form = LoginForm(data)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            try:
                user = User.objects.get(username=username)
                if user.check_password(raw_password=password):
                    token = Token.get_user_token(user=user)
                    return Response(data={'token': token.key}, status=status.HTTP_200_OK)
                else:
                    # TODO error msg password is wrong
                    return Response(status=status.HTTP_400_BAD_REQUEST)
            except User.DoesNotExist:
                # TODO error msg user do not exits
                return Response(status=status.HTTP_400_BAD_REQUEST)


