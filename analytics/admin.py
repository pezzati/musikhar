from django.contrib import admin
from analytics.models import Favorite, Like

admin.site.register(Like)
admin.site.register(Favorite)

from django.contrib import admin

from analytics.models import Tag, TagPost, UserFileHistory

admin.site.register(Tag)
admin.site.register(TagPost)


@admin.register(UserFileHistory)
class UserFileHistoryAdmin(admin.ModelAdmin):
    list_display = (
        'requested_user',
        'owner_user',
        'file_path',
        'date'
    )
