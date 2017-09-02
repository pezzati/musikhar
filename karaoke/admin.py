from django.contrib import admin


from karaoke.models import Karaoke, Line, Genre, Post

from karaoke.models import Karaoke, Line, Genre, Poem


@admin.register(Karaoke)
class KaraokeAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'created_date',
        'genre',
        'rate',
        'rate_count',
        'cover_photo',

    )

    search_fields = (
        'name',
        'genre',
        'singer',

    )

    list_filter = (
        'rate',

    )


@admin.register(Line)
class LineAdmin(admin.ModelAdmin):
    list_display = (
        'karaoke',
        'text',
    )


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'parent'
    )


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'name',
        'recorded_file',
        'karaoke',
        'created_date'
    )

    search_fields = (
        'user',
        'name'
    )

