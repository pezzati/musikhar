# -*- coding: utf-8 -*-

import datetime

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from rest_framework import status
from rest_framework.authentication import BasicAuthentication
# from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import detail_route, list_route
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
# from zeep import Client

from financial.models import BusinessPackage, BankTransaction, CoinTransaction, BazzarTransaction, GiftCode, \
    UserGiftCode
from financial.serializers import BusinessPackageSerializer, CoinTransactionSerializer, BazzarTransactionSerializer, \
    GiftCodeSerializer
from financial.services import Zarinpal
from inventory.serializers import InventorySerializer
from loginapp.auth import CsrfExemptSessionAuthentication
from loginapp.permissions import IsAuthenticatedNotGuest
from musikhar.abstractions.views import PermissionReadOnlyModelViewSet, IgnoreCsrfAPIView
from django.http import HttpResponse
# from django.shortcuts import redirect

from musikhar.utils import app_logger, Errors


class BusinessPackagesViewSet(PermissionReadOnlyModelViewSet):
    serializer_class = BusinessPackageSerializer
    permission_classes = (IsAuthenticatedNotGuest,)
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    # queryset = BusinessPackage.objects.filter(active=True)
    list_cache = False

    def get_queryset(self):
        return BusinessPackage.objects.filter(active=True, platform_type=self.request.device_type, gifted=False)


class Purchase(IgnoreCsrfAPIView):
    # permission_classes = (IsAuthenticated,)

    @method_decorator(login_required())
    def post(self, request):
        serial_number = request.data.get('serial_number')
        if not serial_number:
            # TODO response msg
            return Response(status=status.HTTP_400_BAD_REQUEST)
        package = BusinessPackage.get_package(code=serial_number)
        if not package:
            # TODO response msg
            return Response(status=status.HTTP_404_NOT_FOUND)

        if package.platform_type == BusinessPackage.android and request.market == 'default':
            tran = BazzarTransaction(user=request.user, package=package)
            tran.state = BazzarTransaction.SENT_TO_APP
            tran.save()
            return Response(BazzarTransactionSerializer(instance=tran).data)

        else:
            bank_transaction = BankTransaction.objects.create(user=request.user,
                                                              package=package,
                                                              amount=package.price)
            zarinpal = Zarinpal()
            success, result = zarinpal.pay(amount=package.price,
                                           desc=u'خرید {}'.format(package.name),
                                           email=request.user.email,
                                           mobile=request.user.mobile)
            if success:
                bank_transaction.authority = success
                bank_transaction.state = BankTransaction.SENT_TO_BANK
                bank_transaction.save()
                # return redirect(result)
                return Response(result)
            else:
                # TODO response msg
                return Response(status=status.HTTP_400_BAD_REQUEST)


    # @method_decorator(login_required())
    # @detail_route
    # def bazzar_payment(self, request, sn):
    #     user = request.user
    #     try:
    #         tran = BazzarTransaction.objects.get(serial_number=sn, user=user, package_applied=False)
    #     except:
    #         return Response(status=status.HTTP_404_NOT_FOUND)
    #
    #     if tran.is_valid():
    #         tran.apply_package()
    #         user.refresh_from_db()
    #         return Response(data=dict(coins=user.coins))
    #
    #     return Response(status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        app_logger.info('[BANK_CALL_BACK] time: {} - request: {}'.format(datetime.datetime.now(), request.GET))
        zarinpal = Zarinpal()
        authority = request.GET['Authority']
        bank_transaction = BankTransaction.objects.get(authority=authority)
        if bank_transaction.state == BankTransaction.SUCCESS:
            return HttpResponse()
        bank_transaction.state = BankTransaction.RETURNED
        bank_transaction.save()

        if request.GET.get('Status') == 'OK':
            app_logger.info('[BANK_CALL_BACK] {}, status: OK'.format(datetime.datetime.now()))
            result = zarinpal.verify(request=request, authority=authority, amount=bank_transaction.amount)
            app_logger.info('[BANK_CALL_BACK] {}, result: {}'.format(datetime.datetime.now(), result))
            if not result:
                bank_transaction.state = BankTransaction.CHECK_FAILED
                bank_transaction.save()
                return HttpResponse('Transaction failed. Try again later\nStatus: ' + str(result.Status))
            if result.Status == 100:
                bank_transaction.state = BankTransaction.SUCCESS
                bank_transaction.refId = result.RefID
                bank_transaction.save()
                bank_transaction.apply_package()
                return HttpResponse('Transaction success.\nRefID: ' + str(result.RefID))
            elif result.Status == 101:
                if bank_transaction.state != BankTransaction.SUCCESS:
                    bank_transaction.state = BankTransaction.SUCCESS
                    bank_transaction.refId = result.RefID
                    bank_transaction.save()
                    bank_transaction.apply_package()
                return HttpResponse('Transaction submitted : ' + str(result.Status))
            else:
                bank_transaction.state = BankTransaction.CHECK_FAILED
                bank_transaction.save()
                return HttpResponse('Transaction failed.\nStatus: ' + str(result.Status))
        else:
            app_logger.info('[BANK_CALL_BACK] {}, status: NOK'.format(datetime.datetime.now()))
            bank_transaction.state = BankTransaction.FAILED_BANK
            bank_transaction.save()
            return HttpResponse('Transaction failed or canceled by user')

        # return zarinpal.verify(request=request, authority=authority, amount=bank_transaction.amount)
        # package = BusinessPackage()
        # package.apply_package(user=request.user)
        # return Response()


# MERCHANT = 'XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX'
# client = Client('https://www.zarinpal.com/pg/services/WebGate/wsdl')
# amount = 1000  # Toman / Required
# description = "توضیحات مربوط به تراکنش را در این قسمت وارد کنید"  # Required
# email = 'email@example.com'  # Optional
# mobile = '09123456789'  # Optional
# CallbackURL = 'http://localhost:8000/verify/' # Important: need to edit for realy server.
#
# def send_request(request):
#     result = client.service.PaymentRequest(MERCHANT, amount, description, email, mobile, CallbackURL)
#     if result.Status == 100:
#         return redirect('https://www.zarinpal.com/pg/StartPay/' + str(result.Authority))
#     else:
#         return HttpResponse('Error code: ' + str(result.Status))


class Bazzar(IgnoreCsrfAPIView):
    permission_classes = (IsAuthenticatedNotGuest,)

    def post(self, request):
        sn = request.data.get('serial_number')
        ref_id = request.data.get('ref_id')

        if not ref_id or not sn:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        user = request.user
        try:
            tran = BazzarTransaction.objects.get(serial_number=sn, user=user)
            tran.ref_id = ref_id
            tran.save(update_fields=['ref_id'])
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if tran.is_valid():
            tran.apply_package()
            user.refresh_from_db()
            return Response(data=dict(coins=user.coins))

        return Response(status=status.HTTP_406_NOT_ACCEPTABLE)


class GiftCodeViewSet(PermissionReadOnlyModelViewSet):
    permission_classes = (IsAuthenticatedNotGuest,)
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    serializer_class = GiftCodeSerializer
    queryset = GiftCode.objects.filter(active=True)

    @list_route(methods=['post'])
    def validate(self, request):
        code = request.data.get('code')
        try:
            gift_code = GiftCode.objects.get(code=code)
            if not gift_code.is_valid():
                raise GiftCode.DoesNotExist
        except GiftCode.DoesNotExist:
            errors = Errors.get_errors(Errors, error_list=['Invalid_Code'])
            return Response(data=errors, status=status.HTTP_404_NOT_FOUND)

        try:
            UserGiftCode.objects.get(user=request.user, gift_code=gift_code)
        except UserGiftCode.DoesNotExist:
            return Response(status=status.HTTP_200_OK)

        errors = Errors.get_errors(Errors, error_list=['Used_Code'])
        return Response(data=errors, status=status.HTTP_400_BAD_REQUEST)

    @list_route(methods=['post'])
    def apply(self, request):
        code = request.data.get('code')
        try:
            gift_code = GiftCode.objects.get(code=code)
            if not gift_code.is_valid():
                raise GiftCode.DoesNotExist
        except GiftCode.DoesNotExist:
            errors = Errors.get_errors(Errors, error_list=['Invalid_Code'])
            return Response(data=errors, status=status.HTTP_404_NOT_FOUND)

        try:
            action = UserGiftCode.objects.create(user=request.user, gift_code=gift_code)
        except Exception as e:
            print(str(e))
            errors = Errors.get_errors(Errors, error_list=['Used_Code'])
            return Response(data=errors, status=status.HTTP_400_BAD_REQUEST)

        action.apply()
        return Response(data=InventorySerializer(instance=request.user.inventory).data, status=status.HTTP_200_OK)

