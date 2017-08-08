from django.contrib import admin

from loginapp.models import User, Token

admin.site.register(User)
admin.site.register(Token)
