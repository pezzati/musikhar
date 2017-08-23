from django.db.utils import IntegrityError
from rest_framework.response import Response
from rest_framework import status
from loginapp.models import User, Token
from musikhar.abstractions.views import IgnoreCsrfAPIView
from loginapp.forms import SignupForm, LoginForm
from musikhar.utils import Errors
from django.core.mail import send_mail
from sendsms import  api


class UserSignup(IgnoreCsrfAPIView):

    def post(self, request):
        data = request.data
        form = SignupForm(data)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            email = form.cleaned_data.get('email')
            mobile = form.cleaned_data.get('mobile')

            try:
                user = User.objects.create(username=username)
                user.set_password(raw_password=password)
            except IntegrityError:
                response = Errors.get_errors(Errors, error_list=['Username_Exists'])
                return Response(status=status.HTTP_400_BAD_REQUEST, data=response)

            if form.cleaned_data.get('referrer'):
                user.referred_by = form.cleaned_data.get('referrer')
                user.get_premium_by_referrer_count()
            user.country = 'Iran'

            if email:
                user.email = email
            if mobile:
                user.mobile = mobile
            user.save()

            token = Token.objects.create(user=user)
            return Response(data={'token': token.key}, status=status.HTTP_200_OK)

        response = Errors.get_errors(Errors, error_list=form.error_translator())
        return Response(status=status.HTTP_400_BAD_REQUEST, data=response)


class UserLogin(IgnoreCsrfAPIView):

    def post(self, request):
        data = request.data
        form = LoginForm(data)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            email = form.cleaned_data.get('email')
            mobile = form.cleaned_data.get('mobile')
            try:
                if username is not None:
                    user = User.objects.get(username=username)
                    if user.check_password(raw_password=password):
                            token = Token.get_user_token(user=user)
                            return Response(data={'token': token.key}, status=status.HTTP_200_OK)
                    else:
                            response = Errors.get_errors(Errors, error_list=['Invalid_Login'])
                            return Response(status=status.HTTP_400_BAD_REQUEST, data=response)
                if email is not None:
                    user = User.objects.get(email=email)
                    password = User.objects.make_random_password()
                    user.set_password(raw_password=password)
                    send_mail(
                                'Your Recovery password',
                                'Username :",user.username," password:"user.password".',
                                'from@example.com',
                                ['"user.email"'],
                                fail_silently=False,
                            )
                    return Response(data={'username': user.username, 'password': user.password})

                if mobile is not None:
                    user = User.objects.get(mobile=mobile)
                    password = User.objects.make_random_password()
                    user.set_password(raw_password=password)
                    api.send_sms(body='Username :",user.username," password:"user.password".', from_phone='+41791111111', to=['+41791234567'])
                    return Response(data={'username': user.username, 'password': user.password})


            except User.DoesNotExist:
                response = Errors.get_errors(Errors, error_list=['Invalid_Login'])
                return Response(status=status.HTTP_400_BAD_REQUEST, data=response)

        response = Errors.get_errors(Errors, error_list=form.error_translator())
        return Response(status=status.HTTP_400_BAD_REQUEST, data=response)

