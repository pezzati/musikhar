# -*- coding: utf-8 -*-

import datetime

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from rest_framework import status
from rest_framework.authentication import BasicAuthentication
# from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
# from zeep import Client

from financial.models import BusinessPackage, BankTransaction
from financial.serializers import BusinessPackageSerializer
from financial.services import Zarinpal
from loginapp.auth import CsrfExemptSessionAuthentication
from loginapp.permissions import IsAuthenticatedNotGuest
from musikhar.abstractions.views import PermissionReadOnlyModelViewSet, IgnoreCsrfAPIView
from django.http import HttpResponse
# from django.shortcuts import redirect

from musikhar.utils import app_logger


class BusinessPackagesViewSet(PermissionReadOnlyModelViewSet):
    serializer_class = BusinessPackageSerializer
    permission_classes = (IsAuthenticatedNotGuest,)
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    queryset = BusinessPackage.objects.filter(active=True)
    list_cache = False

    # TODO filter by device_type, get from request.device_type
    # def get_queryset(self):
    #     self.request.user


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

    def get(self, request):
        zarinpal = Zarinpal()
        authority = request.GET['Authority']
        bank_transaction = BankTransaction.objects.get(authority=authority)
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
