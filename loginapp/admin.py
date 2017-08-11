from django.contrib import admin
from karaoke.models import Karaoke, Line
from loginapp.models import User, Token


admin.site.register(User)
admin.site.register(Token)
admin.site.register(Karaoke)
admin.site.register(Line)
