from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from loginapp.forms import DeviceForm
from loginapp.models import Device, User, Token
from musikhar.abstractions.views import IgnoreCsrfAPIView
from loginapp.forms import SignupForm, LoginForm


class DeviceSignUpView(IgnoreCsrfAPIView):
    def post(self, request):
        data = request.data
        form = DeviceForm(data)
        if form.is_valid():
            udid = form.cleaned_data.get('udid')
            device_type = form.cleaned_data.get('type')
            try:
                device = Device.objects.get(udid=udid, type=device_type)
                user = device.user
            except Device.DoesNotExist:
                if request.user.is_authenticated():
                    user = request.user
                else:
                    user = User.objects.create_user(username=udid, password=udid[:15])
                Device.objects.create(
                    udid=udid,
                    type=device_type,
                    os_version=form.cleaned_data.get('os_version'),
                    user=user
                )

            token_list = Token.objects.filter(user=user)
            if len(token_list) == 0:
                token = Token.objects.create(user=user)
            else:
                token = token_list.last()

            return Response(data={'token': token.key})


class UserSignup(IgnoreCsrfAPIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        if request.user.is_signup:
            token = Token.objects.filter(user=request.user).first()
            return Response(data={'token': token.key}, status=status.HTTP_200_OK)

        data = request.data
        form = SignupForm(data)
        user = request.user
        if form.is_valid():
            user.username = form.cleaned_data.get('username')
            user.mobile = form.cleaned_data.get('mobile')
            user.is_signup = True
            user.save()

            token = Token.objects.create(user=user)
            return Response(data={'token': token.key}, status=status.HTTP_200_OK)

        print(form.errors)
        return Response(status=status.HTTP_400_BAD_REQUEST)

class UserLogin(IgnoreCsrfAPIView):
    permission_classes = (IsAuthenticated,)

    def post(self,request):
        data = request.data
        form = LoginForm(data)
        user = request.user
        if form.is_valid():
            user.username = form.cleaned_data.get('username')
            user.mobile = form.cleaned_data.get('mobile')
            user.save
            token = Token.objects.filter(user=request.user).last()
            return Response(data={'token': token.key}, status=status.HTTP_200_OK)
