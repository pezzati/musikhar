from zeep import Client
from django.http import HttpResponse
from django.shortcuts import redirect


class Zarinpal:
    MERCHANT = '978d571e-210a-11e8-a281-000c295eb8fc'
    # client = Client('https://www.zarinpal.com/pg/services/WebGate/wsdl')
    # amount = 1000  # Toman / Required
    # description = "توضیحات مربوط به تراکنش را در این قسمت وارد کنید"  # Required
    # email = 'email@example.com'  # Optional
    # mobile = '09123456789'  # Optional
    CallbackURL = 'http://canto-app.ir/finance/purchase'  # Important: need to edit for realy server.

    def pay(self, amount, desc, email='', mobile=''):
        try:
            result = Client('https://www.zarinpal.com/pg/services/WebGate/wsdl').service.PaymentRequest(self.MERCHANT, amount, desc, email, mobile, self.CallbackURL)
            if result.Status == 100:
                return result.Authority, 'https://www.zarinpal.com/pg/StartPay/{}'.format(result.Authority)
            else:
                return False, str(result.Status)
        except Exception as e:
            return False, str(e)

    def verify(self, request, authority, amount):
        if request.GET.get('Status') == 'OK':
            try:
                result = Client('https://www.zarinpal.com/pg/services/WebGate/wsdl').service.PaymentVerification(self.MERCHANT, authority, amount)
                return result
            except:
                pass
            # if result.Status == 100:
            #     return HttpResponse('Transaction success.\nRefID: ' + str(result.RefID))
            # elif result.Status == 101:
            #     return HttpResponse('Transaction submitted : ' + str(result.Status))
            # else:
            #     return HttpResponse('Transaction failed.\nStatus: ' + str(result.Status))
        else:
            # return HttpResponse('Transaction failed or canceled by user')
            pass
        return
