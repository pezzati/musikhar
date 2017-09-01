from django.contrib import admin

from karaoke.models import Karaoke, Line, Genre, Post


@admin.register(Karaoke)
class KaraokeAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'created_date',
        'genre',
        'rate',
        'rate_count',
        'cover_photo',
        'poem',
        'genre',
        'composer',
        'singer',

    )

    search_fields = (
        'name',
        'genre',
        'singer',

    )


@admin.register(Line)
class LineAdmin(admin.ModelAdmin):
    list_display = (
        'karaoke',
        'text',
        'start_time',
        'end_time'
    )

    search_fields = (
        'karaoke'
    )


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'parent'
    )

    search_fields = (
        'name'
    )


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'name',
        'recorded_file',
        'like_state',
        'karaoke',
        'created_date'
    )

    search_fields = (
        'user',
        'name'
    )
