from django import forms
import re

from loginapp.models import Device
from musikhar.utils import validate_cellphone, validate_email
from musikhar import utils

PROFILE_FORM_ERROR_KEY_MAP = {
    'age': {
        'invalid': 'Invalid_Age',
        'required': 'Missing_Age'
    },
    'mobile': {
        'invalid': 'Invalid_Mobile',
        'required':  'Missing_Mobile'
    },
    'email': {
        'invalid': 'Invalid_Email',
        'required': 'Missing_Email'
    },
    'gender': {
        'invalid': 'Invalid_Gender',
        'required': 'Missing_Gender'
    }
}

DEVICE_FORM_ERROR_KEY_MAP = {
    'udid': {
        'invalid': 'Invalid_Udid',
        'required': 'Missing_Udid'

    },
    'type': {
        'invalid': 'Invalid_Type',
        'required': 'Missing_Type'
    },
    'os_version': {
        'invalid': 'Invalid_Os_Version',
        'required': 'Missing_Os_version'
    }
}

LOGIN_SIGNUP_ERROR_KEY_MAP = {
    'username': {
        'invalid': 'Invalid_Username',
        'required': 'Missing_Username'
    },
    'password': {
        'invalid': 'Invalid_Mobile',
        'required': 'Missing_Mobile'
    },
    'mobile': {
        'invalid': 'Invalid_Mobile',
        'required': 'Missing_Mobile'
    },

    'country': {
        'invalid': 'Invalid_Mobile',
        'required': 'Missing_Mobile'
    }

}

default_error_messages = {'required': 'required', 'invalid': 'invalid', 'invalid_choice': 'invalid'}


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
                raise forms.ValidationError('mobile')
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
    username = forms.CharField(max_length=50)
    mobile = forms.CharField(max_length=20)
    password = forms.CharField(max_length=30)
    country = forms.CharField(max_length=30)

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

    def clean_password(self):

        password = self.cleaned_data.get('password')
        if password :
            return password
        else:
            raise forms.ValidationError('invalid')

    def clean_country(self):
        country = self.cleaned_data.get('country')
        if country:
            return country
        else:
            raise forms.ValidationError('invalid')


class LoginForm(forms.Form):

    username = forms.CharField(max_length=50)
    mobile = forms.CharField(max_length=20)
    password = forms.CharField(max_length=30)

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

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if password:
            return password
        else:
            raise forms.ValidationError('invalid')
