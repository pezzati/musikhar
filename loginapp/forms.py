from django import forms

from musikhar.utils import validate_cellphone, validate_email


class ProfileForm(forms.Form):
    password = forms.CharField(required=False, max_length=50)
    email = forms.CharField(required=False, max_length=50)
    mobile = forms.CharField(required=False, max_length=20)
    gender = forms.IntegerField(required=False)
    age = forms.IntegerField(required=False)

    def clean_age(self):
        age = self.cleaned_data.get('age')
        if age < 0 or age > 100:
            raise forms.ValidationError('invalid')
        return age

    def clean_mobile(self):
        mobile = self.cleaned_data.get('mobile')
        mobile = validate_cellphone(mobile)
        if not mobile:
            raise forms.ValidationError('mobile must be just numbers')
        return mobile

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if validate_email(email):
            raise forms.ValidationError('invalid')
        return email

    def clean_gender(self):
        gender = self.cleaned_data.get('gender')
        if gender == 0 or gender == 1:
            return gender
        raise forms.ValidationError('invalid')
