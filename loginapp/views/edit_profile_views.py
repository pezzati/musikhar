import json
from django import forms

from django.views.generic.base import View

from loginapp.auth import if_authorized
from loginapp.models import User
from rest_framework.response import Response



@if_authorized
def update_user_profile(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user = request.user


        if data.get('username'):
            user.username = data.get('username')

        if data.get('password'):
            user.set_password()

        if data.get('email'):
            user.email = data.get('email')

        if data.get('mobile'):
            user.mobile = data.get('mobile')

        if data.get('gender'):
            user.gender = data.get('gender')

        if data.get('age') :
            user.age = data.get('age')




class ProfileView(View):

    @method_decorator(if_authorized)
    def dispatch(self, request, *args, **kwargs):
        return super(ProfileView, self).dispatch(request=request, *args, **kwargs)


    def post(self, request):
        user = request.user




    def get(self, request):
     return True




class Profile_Form(forms.Form):
    male = 0
    female = 1
    GenderTypes = (
        (male, 'Male'),
        (female, 'Female')
    )
    password = forms.CharField(max_length=50)
    email = forms.CharField(max_length=50)
    mobile = forms.CharField(max_length=20)
    gender = forms.IntegerField(widget=forms.Select(choices= GenderTypes))
    age = forms.IntegerField()

    def full_clean(self):



