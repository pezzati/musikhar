import json
import random
import string

from django.test import TestCase
from django.test.client import Client

from loginapp.models import User, Device, Token


class TestSignUp(TestCase):

    @staticmethod
    def generate_random(length=40):
        return ''.join(
                random.SystemRandom().choice(string.ascii_uppercase + string.digits + string.ascii_lowercase) for _ in
                range(length))

    def setUp(self):
        self.client = Client()

    def send_device_signup(self, device_type):
        url = '/user/device_signup'
        udid = self.generate_random(40)
        body = {
            'udid': udid,
            'type': device_type,
            'os_version': 12,
        }
        response = self.client.post(
            url,
            data=json.dumps(body),
            content_type='application/json',
        )
        self.assertEqual(response.status_code, 200)

        self.assertEqual(len(User.objects.filter(username=udid)), 1)
        user = User.objects.get(username=udid)
        self.assertEqual(len(Device.objects.filter(udid=udid, type=device_type, user=user, os_version=12)), 1)
        self.assertEqual(len(Token.objects.filter(user=user)), 1)
        token = Token.objects.get(user=user)

        response_body = response.data
        self.assertEqual(response_body.get('token'), token.key)

    def test_device_signup(self):
        self.send_device_signup(device_type=Device.ios)
        self.send_device_signup(device_type=Device.android)
