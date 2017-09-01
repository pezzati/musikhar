from django.contrib import admin
from loginapp.models import User, Token, Follow, Artist


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'name',
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
        'user'
    )

    list_filter = (
        'created_date'
    )


@admin.register(Follow)
class FollowAdmin:
    list_display = (
        'follower'
        'created_date'
    )

    search_fields = (
        'follower',
        'following'
    )

    list_filter = (
        'created_date'
    )

    
@admin.register(Artist)
class ArtistAdmin:

    list_display = (
        'user',
        'name',
    )

    search_fields = (
        'user',
        'name'
    )

    list_filter = (
        'name'
    )
