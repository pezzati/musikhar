from django.contrib import admin
from analytics.models import Favorite, Like

admin.site.register(Like)
admin.site.register(Favorite)

from django.contrib import admin

from analytics.models import Tag, TagPost

admin.site.register(Tag)
admin.site.register(TagPost)
