from django.contrib import admin
from loginapp.models import User, Token, Follow


admin.site.register(User)
admin.site.register(Token)
admin.site.register(Follow)
