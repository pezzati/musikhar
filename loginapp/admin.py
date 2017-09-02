from django.contrib import admin
from loginapp.models import User, Token, Follow, Artist


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'username',
        'password',
        'email',
        'mobile',
        'image',
        'birth_date',
        'country',
        'get_referred_by',
    )

    search_fields = (
        'name',
        'email',
        'mobile',

    )

    list_filter = (
        'birth_date',
        'country'
    )


@admin.register(Token)
class TokenAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'key',
    )

    search_fields = (
        'user',
    )


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = (
        'follower',
        'followed'

    )

    search_fields = (
        'follower',
        'followed'

    )


@admin.register(Artist)
class ArtistAdmin(admin.ModelAdmin):

    list_display = (
        'user',
        'name',
    )

    search_fields = (
        'user',
    )


