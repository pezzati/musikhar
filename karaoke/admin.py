from django.contrib import admin

<<<<<<< HEAD
from karaoke.models import Karaoke, Line, Genre, Post
=======
from karaoke.models import Karaoke, Line, Genre, Poem
>>>>>>> develop


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
        'created_date',
        'rate',

    )


@admin.register(Line)
class LineAdmin(admin.ModelAdmin):
    list_display = (
        'karaoke',
        'text',
    )


<<<<<<< HEAD
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

=======
admin.site.register(Line)
admin.site.register(Genre)
admin.site.register(Poem)
>>>>>>> develop
