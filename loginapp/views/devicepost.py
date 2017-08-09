from loginapp.forms import DeviceForm
from rest_framework.response import Response
from musikhar.abstractions.views import IgnoreCsrfAPIView
from loginapp.serializers import DeviceSerilalizer
from loginapp.models import User, Token, Device


class DevicePost(IgnoreCsrfAPIView):

    def post(self, request):
        data = request.data
        form = DeviceForm(data)
        if form.is_valid():
            udid = form.cleaned_data.get('udid')
            device_type = form.cleaned_data.get('type')
            try:
                device = Device.objects.filter(udid=udid, type=device_type)
                user = device.user
            except Device.DoesNotExist:
                print('yesß')

