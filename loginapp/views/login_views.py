from django.db.utils import IntegrityError
from rest_framework.response import Response
from rest_framework import status
from loginapp.models import User, Token
from musikhar.abstractions.views import IgnoreCsrfAPIView
from loginapp.forms import SignupForm, LoginForm
from musikhar.utils import Errors, app_logger


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
            app_logger.info('[SIGN_UP_RES] user: {} - token: {}'.format(user.username, token.key))
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
            try:
                user = User.objects.get(username=username)
                if user.check_password(raw_password=password):
                        token = Token.get_user_token(user=user)
                        return Response(data={'token': token.key}, status=status.HTTP_200_OK)
                else:
                        response = Errors.get_errors(Errors, error_list=['Invalid_Login'])
                        return Response(status=status.HTTP_400_BAD_REQUEST, data=response)

            except User.DoesNotExist:
                response = Errors.get_errors(Errors, error_list=['Invalid_Login'])
                return Response(status=status.HTTP_400_BAD_REQUEST, data=response)

        response = Errors.get_errors(Errors, error_list=form.error_translator())
        return Response(status=status.HTTP_400_BAD_REQUEST, data=response)


class PasswordRecovery(IgnoreCsrfAPIView):
    def post(self, request):
        data = request.data
        email = data.get('email')
        mobile = data.get('mobile')

        if not mobile and not email:
            response = Errors.get_errors(Errors, error_list=['Missing_Form'])
            return Response(status=status.HTTP_400_BAD_REQUEST, data=response)

        try:
            if email:
                user = User.objects.get(email=email)
                password = User.objects.make_random_password()
                print(password)
                user.set_password(raw_password=password)
                user.send_email_recovery_password()
                return Response(status=status.HTTP_200_OK)

            if mobile:
                user = User.objects.get(mobile=mobile)
                password = User.objects.make_random_password()
                print(password)
                user.set_password(raw_password=password)
                user.send_sms_recovery_password()
                return Response(status=status.HTTP_200_OK)

        except User.DoesNotExist:
            response = Errors.get_errors(Errors, error_list=['User_Not_Found'])
            return Response(status=status.HTTP_400_BAD_REQUEST, data=response)

