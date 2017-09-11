from django.contrib import admin
from loginapp.models import User, Token, Follow, Artist

admin.site.register(User)
admin.site.register(Artist)


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = (
        'follower',
        'followed'
    )

    readonly_fields = (
        'follower',
        'followed'
    )


@admin.register(Token)
class TokenAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'key',
        'created'
    )

    readonly_fields = (
        'user',
        'key',
        'created'
    )
