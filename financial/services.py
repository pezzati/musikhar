from zeep import Client
from django.http import HttpResponse
from django.shortcuts import redirect


class Zarinpal:
    MERCHANT = 'XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX'
    client = Client('https://www.zarinpal.com/pg/services/WebGate/wsdl')
    # amount = 1000  # Toman / Required
    # description = "توضیحات مربوط به تراکنش را در این قسمت وارد کنید"  # Required
    # email = 'email@example.com'  # Optional
    # mobile = '09123456789'  # Optional
    CallbackURL = 'http://localhost:8000/verify/'  # Important: need to edit for realy server.

    def pay(self, amount, desc, email='', mobile=''):
        params = [self.MERCHANT, amount, desc]
        if email:
            params.append(email)
        if mobile:
            params.append(mobile)
        params.append(self.CallbackURL)
        result = self.client.service.PaymentRequest(*params)
        if result.Status == 100:
            return result.Authority, 'https://www.zarinpal.com/pg/StartPay/{}'.format(result.Authority)
        else:
            return False, str(result.Status)

    def verify(self, request, amount):
        if request.GET.get('Status') == 'OK':
            result = self.client.service.PaymentVerification(self.MERCHANT, request.GET['Authority'], amount)
            if result.Status == 100:
                return HttpResponse('Transaction success.\nRefID: ' + str(result.RefID))
            elif result.Status == 101:
                return HttpResponse('Transaction submitted : ' + str(result.Status))
            else:
                return HttpResponse('Transaction failed.\nStatus: ' + str(result.Status))
        else:
            return HttpResponse('Transaction failed or canceled by user')
