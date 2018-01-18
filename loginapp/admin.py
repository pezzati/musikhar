from django.contrib import admin
from loginapp.models import User, Token, Follow, Artist, Verification

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


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    search_fields = ('username', 'mobile', 'email')
    list_display = ('username', 'mobile', 'email')
    filter_horizontal = ('genres',)


admin.site.register(Verification)


