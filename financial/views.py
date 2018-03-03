from rest_framework import status
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from zeep import Client

from financial.models import BusinessPackage, BankTransaction
from financial.serializers import BusinessPackageSerializer
from financial.services import Zarinpal
from loginapp.auth import CsrfExemptSessionAuthentication
from musikhar.abstractions.views import PermissionReadOnlyModelViewSet, IgnoreCsrfAPIView
from django.http import HttpResponse
from django.shortcuts import redirect


class BusinessPackagesViewSet(PermissionReadOnlyModelViewSet):
    serializer_class = BusinessPackageSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    queryset = BusinessPackage.objects.filter(active=True)
    list_cache = False


class Purchase(IgnoreCsrfAPIView):
    permission_classes = (IsAuthenticated,)

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
        sucess, result = zarinpal.pay(amount=package.price,
                                      desc='kharide baste',
                                      email=request.user.email,
                                      mobile=request.user.mobile)
        if sucess:
            bank_transaction.authority = sucess
            bank_transaction.state=BankTransaction.SENT_TO_BANK
            bank_transaction.save()
            return redirect(sucess)
        else:
            # TODO response msg
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        if request.GET.get('Status') == 'OK':
            pass
        package = BusinessPackage()
        package.apply_package(user=request.user)
        return Response()


MERCHANT = 'XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX'
client = Client('https://www.zarinpal.com/pg/services/WebGate/wsdl')
amount = 1000  # Toman / Required
description = "توضیحات مربوط به تراکنش را در این قسمت وارد کنید"  # Required
email = 'email@example.com'  # Optional
mobile = '09123456789'  # Optional
CallbackURL = 'http://localhost:8000/verify/' # Important: need to edit for realy server.

def send_request(request):
    result = client.service.PaymentRequest(MERCHANT, amount, description, email, mobile, CallbackURL)
    if result.Status == 100:
        return redirect('https://www.zarinpal.com/pg/StartPay/' + str(result.Authority))
    else:
        return HttpResponse('Error code: ' + str(result.Status))
