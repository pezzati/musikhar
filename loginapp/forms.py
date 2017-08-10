from django import forms
import re

from loginapp.models import Device
from musikhar.utils import validate_cellphone, validate_email
from musikhar import utils



class ProfileForm(forms.Form):
    password = forms.CharField(required=False, max_length=50)
    email = forms.CharField(required=False, max_length=50)
    mobile = forms.CharField(required=False, max_length=20)
    gender = forms.IntegerField(required=False)
    age = forms.IntegerField(required=False)

    def clean_age(self):
        age = self.cleaned_data.get('age')
        if age and age < 0 or age > 100:
            raise forms.ValidationError('invalid')
        return age

    def clean_mobile(self):
        mobile = self.cleaned_data.get('mobile')
        if mobile:
            mobile = validate_cellphone(mobile)
            if not mobile:
                raise forms.ValidationError('mobile must be just numbers')
        return mobile

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email:
            if validate_email(email):
                raise forms.ValidationError('invalid')
        return email

    def clean_gender(self):
        gender = self.cleaned_data.get('gender')
        if gender:
            if gender == 0 or gender == 1:
                return gender
            raise forms.ValidationError('invalid')
        else:
            gender = 0
        return gender


class DeviceForm(forms.Form):
    udid = forms.CharField(max_length=200)
    type = forms.CharField(max_length=10)
    os_version = forms.IntegerField()

    def clean_udid(self):

        udid = self.cleaned_data.get('udid')
        if len(udid) != 40:
            raise forms.ValidationError('invalid')

        return udid

    def clean_type(self):
        type = self.cleaned_data.get('type')
        if type != Device.ios and type != Device.android:
            raise forms.ValidationError('invalid')

        return type

    def clean_os_version(self):
        os_version = self.cleaned_data.get('os_version')
        if not os_version:
            os_version = 0

        return os_version


class SignupForm(forms.Form):
    username = forms.CharField(max_length=50 )
    mobile = forms.CharField(max_length=20)

    def clean_username(self):
        username = self.cleaned_data.get('username')
        USERNAME_RE = re.compile(r"(^[a-zA-Z0-9_.-]+$)")
        if not USERNAME_RE.match(username):
            raise forms.ValidationError('invalid')
        return username

    def clean_mobile(self):
        mobile = self.cleaned_data.get('mobile')
        mobile = utils.validate_cellphone(mobile)
        if mobile:
            return mobile
        else:
            raise forms.ValidationError('invalid')
