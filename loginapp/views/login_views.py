from time import sleep

import requests
import json
from datetime import datetime, timedelta

from django.conf import settings
from django.utils import six, timezone
from rest_framework.response import Response
from rest_framework import status

from financial.models import UserPaymentTransaction, CoinTransaction
from loginapp.models import User, Token, Verification, Device
from loginapp.serializers import UserInfoSerializer
from musikhar.abstractions.views import IgnoreCsrfAPIView
from loginapp.forms import SignupForm
from musikhar.middlewares import error_logger
from musikhar.utils import Errors, conn, get_not_none, app_logger, PLATFORM_ANDROID


class UserSignup(IgnoreCsrfAPIView):

    def post(self, request):
        data = request.data
        form = SignupForm(data)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            mobile = form.cleaned_data.get('mobile')

            username = mobile if mobile else email
            username = username.lower()

            if request.user and not request.user.is_anonymous:
                user = request.user
            else:
                user = User.get_user(username=username, mobile=username, email=username)

            if not user or user.is_guest:
                if not user:
                    password = User.objects.make_random_password()
                    user = User.objects.create(username=username)
                    user.set_password(raw_password=password)
                    conn().set(name=username, value='new_user')
                else:
                    user.username = username
                    user.signup_date = timezone.now()
                    user.is_guest = False

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
            email = email.lower()
        except:
            pass
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
            user = User.get_user(username=mobile_or_phone, mobile=mobile_or_phone, email=mobile_or_phone)
            if user is None:
                raise User.DoesNotExist
            verification = Verification.objects.get(code=code, user=user)
        except Verification.DoesNotExist:
            response = Errors.get_errors(Errors, error_list=['Invalid_Token'])
            return Response(status=status.HTTP_400_BAD_REQUEST, data=response)
        except User.DoesNotExist:
            response = Errors.get_errors(Errors, error_list=['User_Not_Found'])
            return Response(status=status.HTTP_400_BAD_REQUEST, data=response)

        user = verification.user
        if verification.type == Verification.SMS_CODE:
            user.mobile_confirmed = True
        elif verification.type == Verification.EMAIL_CODE:
            user.email_confirmed = True

        user.save()

        if 'udid' in data:
            udid = get_not_none(data, 'udid', 'not-set')
            bundle = get_not_none(data, 'bundle', 'com.application.canto')
            try:
                Device.objects.get(udid=udid,
                                   bundle=bundle,
                                   user=user
                                   )
                d = Device.objects.filter(udid=udid, bundle=bundle, user__isnull=True).first()
                if d:
                    d.delete()
            except Device.DoesNotExist:
                # TODO fix this hit
                try:
                    d = Device.objects.filter(udid=udid, bundle=bundle, user__isnull=True).first()
                    d.user = user
                    d.save()
                except:
                    d = Device.objects.create(udid=udid, bundle=bundle)
                    d.user = user
                    d.save()

        token = Token.generate_token(user=user)
        res_data = {'token': token.key,
                    'new_user': False,
                    'user': None
                    }

        new_user = conn().get(name=user.username)
        if new_user and new_user == b'new_user':
            tran = CoinTransaction.objects.create(user=user, coins=500, amount=0)
            tran.apply()
            res_data['new_user'] = True
            conn().delete(user.username)

        res_data['user'] = UserInfoSerializer(instance=user, context={'request': request, 'caller': User}).data

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
GOOGLE_CLIENT_ID_ANDROID = 'AIzaSyCvss0J0H1pPb3J9vwgvaWY4Uc35DpySW4'

'''
{
    "iss": "https://accounts.google.com",
    "azp": "846781616423-aq2btcme7fvklrohvfoukr5mleg373di.apps.googleusercontent.com",
    "aud": "846781616423-v3f92os3p2m4m7ckf918f9orjahmdqaf.apps.googleusercontent.com",
    "sub": "103088112241416255161",
    "email": "hamed.ma7@gmail.com",
    "email_verified": "true",
    "name": "Hamed Momeni",
    "picture": "https://lh3.googleusercontent.com/-RIPG9o61A-w/AAAAAAAAAAI/AAAAAAAAFE0/SgqvEb2I52M/s96-c/photo.jpg",
    "given_name": "Hamed",
    "family_name": "Momeni",
    "locale": "en",
    "iat": "1548170903",
    "exp": "1548174503",
    "alg": "RS256",
    "kid": "08d3245c62f86b6362afcbbffe1d069826dd1dc1",
    "typ": "JWT"
}
'''


class SignupGoogle(IgnoreCsrfAPIView):
    def post(self, request):
        # from google.oauth2 import id_token
        # from google.auth.transport import requests
        created = False
        token = request.data.get('token')

        try:
            # Specify the CLIENT_ID of the app that accesses the backend:
            # if request.device_type == PLATFORM_ANDROID:
            #     error_logger.info('[GOOGLE_SIGNUP] android')
            #     idinfo = id_token.verify_oauth2_token(token, requests.Request(), GOOGLE_CLIENT_ID_ANDROID)
            # else:
            #     idinfo = id_token.verify_oauth2_token(token, requests.Request(), GOOGLE_CLIENT_ID)
            # Or, if multiple clients access the backend server:
            # idinfo = id_token.verify_oauth2_token(token, requests.Request())
            # if idinfo['aud'] not in [CLIENT_ID_1, CLIENT_ID_2, CLIENT_ID_3]:
            #     raise ValueError('Could not verify audience.')

            tries = 3
            while tries >= 0:
                try:
                    url = 'https://www.googleapis.com/oauth2/v3/tokeninfo?id_token={}'.format(token)
                    response = requests.get(url, timeout=30)
                    if int(response.status_code / 100) != 2:
                        error_logger.info('[GOOGLE_SIGNUP_NON_200] time: {}, {}'.format(datetime.now(),
                                                                                        response.status_code,))
                        try:
                            error_logger.info('[GOOGLE_SIGNUP_NON_200_CONTENT] {}'.format(request.content))
                            error_logger.info('[GOOGLE_SIGNUP_NON_200_CONTENT_RES] {}'.format(response.content))

                        except:
                            pass
                        try:
                            error_logger.info('[GOOGLE_SIGNUP_NON_200_BODY] {}'.format(request.body))
                            error_logger.info('[GOOGLE_SIGNUP_NON_200_BODY_RES] {}'.format(response.body))

                        except:
                            pass
                        try:
                            error_logger.info('[GOOGLE_SIGNUP_NON_200_DATA] {}'.format(request.data))
                            error_logger.info('[GOOGLE_SIGNUP_NON_200_DATA_RES] {}'.format(response.data))

                        except:
                            pass

                        return Response(status=response.status_code)
                except Exception as e:
                    if tries == 0:
                        raise e
                    tries -= 1
                    sleep(0.1)

            idinfo = json.loads(response.content.decode('utf-8'))

            if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
                raise ValueError('Wrong issuer.')

            # If auth request is from a G Suite domain:
            # if idinfo['hd'] != GSUITE_DOMAIN_NAME:
            #     raise ValueError('Wrong hosted domain.')

            # ID token is valid. Get the user's Google Account ID from the decoded token.
            userid = idinfo['sub']
            # user, created = User.objects.get_or_create(email=idinfo['email'], email_confirmed=True)
            try:
                user = User.objects.get(username=idinfo['email'])
            except User.DoesNotExist:
                try:
                    user = User.objects.get(email=idinfo['email'])
                except User.DoesNotExist:
                    created = True

            # user = User.get_user(username=idinfo['email'], email=idinfo['email'])

            if created:
                error_logger.info('[GOOGLE_SIGNUP_DATA] time: {}, {}'.format(datetime.now(), idinfo))
                user = User.objects.create(username=idinfo['email'], email=idinfo['email'])
                user.set_password(raw_password=User.objects.make_random_password())
                user.save()
                created = True
                tran = CoinTransaction.objects.create(user=user, coins=500, amount=0)
                tran.apply()
                # user.username = idinfo['email']
                # user.set_password(User.objects.make_random_password())

            if not user.first_name and idinfo.get('given_name'):
                user.first_name = idinfo.get('given_name')
            if not user.last_name and idinfo.get('family_name'):
                user.last_name = idinfo.get('family_name')

            user.save()

            token = Token.generate_token(user=user)
            res_data = {'token': token.key, 'new_user': created}

            return Response(status=status.HTTP_200_OK, data=res_data)
        except Exception as e:
            error_logger.info('[GOOGLE_SIGNUP] time: {}, {}'.format(datetime.now(), str(e)))
            return Response(status=status.HTTP_400_BAD_REQUEST, data=[{'error': str(e)}])


class NassabCallBack(IgnoreCsrfAPIView):
    def post(self, request):
        data = request.data
        app_logger.info('[NASSAB] DATA: {}'.format(data))

        try:
            email = data['email']
            password = data.get('password')
            days = int(data['days'])
            amount = data['amount']
            tranID = data['transactionId']
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(email=email)
            c = False
        except:
            user = User.objects.create(email=email, username=email)
            c = True
            user.set_password(raw_password=password)

        if c:
            user.username = email
            user.first_name = email.split('@')[0][:30]

        user.save()
        try:
            if tranID == 'redeem':
                payment = UserPaymentTransaction.objects.create(user=user, days=days, amount=amount,
                                                                transaction_info=tranID)
            else:
                payment = UserPaymentTransaction.objects.get(transaction_info=tranID, user=user)
        except UserPaymentTransaction.DoesNotExist:
            payment = UserPaymentTransaction.objects.create(user=user, days=days, amount=amount,
                                                            transaction_info=tranID)

        payment.apply()

        return Response(status=status.HTTP_200_OK)


class NassabLogin(IgnoreCsrfAPIView):

    def get_nassab_user_info(self, email, retry=True):
        if settings.DEBUG:
            return {'transactions': [], 'has_app': True, 'is_premium': True}
        url = 'http://nassaab.com/api/canto/userStatus.php?email={}'.format(email)
        response = requests.get(url)
        if response.status_code not in [200, 201]:
            if retry:
                return self.get_nassab_user_info(email=email, retry=False)
            return None
        try:
            data = json.loads(response.content.decode('utf-8'))
        except Exception as e:
            error_logger.info('[NASSAB_USER_INFO] cant parse content: {}'.format(data))
            return None
        return data

    def post(self, request):
        data = request.data
        bundle = data.get('bundle')
        udid = data.get('udid')
        email = data.get('email')

        if 'nassab.application.canto' not in bundle:
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE)

        user_info = self.get_nassab_user_info(email=email)
        if user_info is None or not user_info.get('has_app'):
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE)

        try:
            user = User.objects.get(email=email)
            c = False
        except:
            user = User.objects.create(email=email, username=email)
            c = True

        if c:
            user.username = email
            user.first_name = email.split('@')[0][:30]
            user.set_password(User.objects.make_random_password())
            user.save()

        if user_info.get('is_premium'):
            if not user.is_premium:
                # TODO set
                user.premium_time = datetime.now() + timedelta(days=1)
                pass
            user.is_premium = True
            user.save()

        Device.objects.get_or_create(udid=udid, bundle=bundle, defaults={'user': user})

        token = Token.generate_token(user=user)
        return Response(data={'token': token.key, 'new_user': False})
