from django.contrib import admin
from analytics.models import Favorite, Like, Banner, Tag, TagPost, UserFileHistory

admin.site.register(Like)
admin.site.register(Favorite)
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


@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'index',
        'is_active',
        'start_time',
        'end_time',
        'clicked_count',
        'link'
    )

    list_editable = (
        'is_active',
        'index'
    )

    readonly_fields = ('clicked_count',)
