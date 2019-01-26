import requests
import json

from datetime import datetime
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
    CallbackURL = 'https://canto-app.ir/finance/purchase'  # Important: need to edit for realy server.

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


class BazzarClient:
    # https://test.canto-app.ir/bazzar?code=8chneTplITHGXtRlTRYdaBlsz02zii
    # {
    #     "access_token": "xxs45AYwKH1vPqLUVfCUbN8Vvtc0y4",
    #     "token_type": "Bearer",
    #     "expires_in": 3600000,
    #     "refresh_token": "RdSXOJH8gVgLPqoLSfNGpD6R5lszHK",
    #     "scope": "androidpublisher"
    # }

    # {
    #     "consumptionState": 0,
    #     "purchaseState": 0,
    #     "kind": "androidpublisher#inappPurchase",
    #     "developerPayload": "TEST_PAYLOAD",
    #     "purchaseTime": 1546259797880
    # }
    ACCESS_TOKEN = 'xxs45AYwKH1vPqLUVfCUbN8Vvtc0y4'
    MASTER_CODE = '8chneTplITHGXtRlTRYdaBlsz02zii'
    PACKAGE_NAME = 'ir.canto_app.android'

    def check_purchase(self, purchase_id, product_id):
        url = 'https://pardakht.cafebazaar.ir/devapi/v2/api/validate/{}/inapp/{}/purchases/{}'.format(self.PACKAGE_NAME,
                                                                                                      product_id,
                                                                                                      purchase_id)
        response = requests.get(url=url, headers={'Authorization': self.ACCESS_TOKEN})

        if response.status_code / 100 != 2:
            return False, None

        data = json.loads(response.content.decode('utf-8'))
        if data.get('purchaseState') == 0:
            return True, datetime.fromtimestamp(data['purchaseTime']/1000)

        return False, None
