# import binascii
import os

from datetime import datetime

from rest_framework.response import Response
from rest_framework import status

from financial.models import UserPaymentTransaction
from loginapp.models import User, Token, Verification, Device
from musikhar.abstractions.views import IgnoreCsrfAPIView
from loginapp.forms import SignupForm
from musikhar.middlewares import error_logger
from musikhar.utils import Errors, conn, get_not_none


class UserSignup(IgnoreCsrfAPIView):

    def post(self, request):
        data = request.data
        form = SignupForm(data)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            mobile = form.cleaned_data.get('mobile')

            username = mobile if mobile else email
            user = User.get_user(username=username)
            if not user:

                password = User.objects.make_random_password()
                user = User.objects.create(username=username)
                user.set_password(raw_password=password)

                if form.cleaned_data.get('referrer'):
                    user.referred_by = form.cleaned_data.get('referrer')
                    user.get_premium_by_referrer_count()
                user.country = 'Iran'

                if email:
                    email = email.lower()
                    user.email = email
                    user.email_confirmed = False
                if mobile:
                    user.mobile = mobile
                    user.mobile_confirmed = False
                user.save()

                conn().set(name=username, value='new_user')
            if email:
                user.send_email_verification()
            if mobile:
                user.send_mobile_verification()
            # token = Token.objects.create(user=user)
            # app_logger.info('[SIGN_UP_RES] user: {} - token: {}'.format(user.username, token.key))
            # return Response(data={'token': token.key}, status=status.HTTP_200_OK)
            return Response(status=status.HTTP_200_OK, data={'username': user.username})

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
                user.set_password(raw_password=password)
                user.send_email_recovery_password()
                return Response(status=status.HTTP_200_OK)

            if mobile:
                user = User.objects.get(mobile=mobile)
                password = User.objects.make_random_password()
                user.set_password(raw_password=password)
                user.send_sms_recovery_password()
                return Response(status=status.HTTP_200_OK)

        except User.DoesNotExist:
            response = Errors.get_errors(Errors, error_list=['User_Not_Found'])
            return Response(status=status.HTTP_400_BAD_REQUEST, data=response)


class Verify(IgnoreCsrfAPIView):
    # permission_classes = (IsAuthenticated,)

    def post(self, request):
        data = request.data
        code = data.get('code')
        if not code:
            response = Errors.get_errors(Errors, error_list=['Invalid_Info'])
            return Response(status=status.HTTP_400_BAD_REQUEST, data=response)

        mobile_or_phone = request.data.get('mobile')
        if mobile_or_phone is None or not mobile_or_phone:
            mobile_or_phone = request.data.get('email')
        try:
            verification = Verification.objects.get(code=code, user__username=mobile_or_phone)
        except Verification.DoesNotExist:
            response = Errors.get_errors(Errors, error_list=['Invalid_Token'])
            return Response(status=status.HTTP_400_BAD_REQUEST, data=response)

        user = verification.user
        if verification.type == Verification.SMS_CODE:
            user.mobile_confirmed = True
        elif verification.type == Verification.EMAIL_CODE:
            user.email_confirmed = True

        user.save()

        udid = get_not_none(data, 'udid', 'not-set')
        bundle = get_not_none(data, 'bundle', 'com.application.canto')
        Device.objects.update_or_create(udid=udid,
                                        bundle=bundle,
                                        defaults={'user': request.user}
                                        )
        # TODO make user premium date
        if 'nassab' in bundle:
            transaction = UserPaymentTransaction.objects.create(user=user,
                                                                days=7,
                                                                amount=12000)
            transaction.apply()

        token = Token.generate_token(user=user)
        res_data = {'token': token.key, 'new_user': False}

        new_user = conn().get(name=user.username)
        if new_user and new_user == b'new_user':
            res_data['new_user'] = True
            conn().delete(user.username)

        if verification.type == Verification.SMS_CODE:
            conn().delete('sms#{}'.format(user.mobile))
        if verification.type == Verification.EMAIL_CODE:
            conn().delete('email#{}'.format(user.email))
        verification.delete()

        return Response(status=status.HTTP_200_OK, data=res_data)

    def get(self, request):
        # user = request.user
        context = request.GET.get('context')
        username = request.GET.get('username')
        user = User.objects.get(username=username)

        if context == 'mobile':
            if user.mobile:
                user.send_mobile_verification(
                    code=Verification.objects.filter(type=Verification.SMS_CODE, user=user).first())
            elif not user.mobile:
                response = Errors.get_errors(Errors, error_list=['No_Mobile'])
                return Response(status=status.HTTP_400_BAD_REQUEST, data=response)
        elif context == 'email':
            if user.email:
                user.send_email_verification(
                    code=Verification.objects.filter(type=Verification.EMAIL_CODE, user=user).first())
            elif not user.email:
                response = Errors.get_errors(Errors, error_list=['No_Email'])
                return Response(status=status.HTTP_400_BAD_REQUEST, data=response)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(status=status.HTTP_200_OK)


GOOGLE_CLIENT_ID = '243773746715-ahsopgmn3jfvqthmkn32mi75lbc69hso.apps.googleusercontent.com'


class SignupGoogle(IgnoreCsrfAPIView):
    def post(self, request):
        from google.oauth2 import id_token
        from google.auth.transport import requests

        token = request.data.get('token')

        try:
            # Specify the CLIENT_ID of the app that accesses the backend:
            idinfo = id_token.verify_oauth2_token(token, requests.Request(), GOOGLE_CLIENT_ID)
            # Or, if multiple clients access the backend server:
            # idinfo = id_token.verify_oauth2_token(token, requests.Request())
            # if idinfo['aud'] not in [CLIENT_ID_1, CLIENT_ID_2, CLIENT_ID_3]:
            #     raise ValueError('Could not verify audience.')

            if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
                raise ValueError('Wrong issuer.')

            # If auth request is from a G Suite domain:
            # if idinfo['hd'] != GSUITE_DOMAIN_NAME:
            #     raise ValueError('Wrong hosted domain.')

            # ID token is valid. Get the user's Google Account ID from the decoded token.
            userid = idinfo['sub']
            user, created = User.objects.get_or_create(email=idinfo['email'], email_confirmed=True)
            if created:
                user.username = idinfo['email']
                password = binascii.hexlify(os.urandom(16)).decode()
                user.set_password(password)
                user.save()

            token = Token.generate_token(user=user)
            res_data = {'token': token.key, 'new_user': created}

            return Response(status=status.HTTP_200_OK, data=res_data)
        except Exception as e:
            error_logger.info('[GOOGLE_SIGNUP] timee: {}, {}'.format(datetime.now(), str(e)))
            # print(str(e))
            return Response(status=status.HTTP_400_BAD_REQUEST)
