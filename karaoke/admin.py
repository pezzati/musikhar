from django.contrib import admin

from analytics.models import TagPost
from karaoke.models import Song, Genre, Poem


class TagInline(admin.TabularInline):
    model = TagPost
    extra = 1


class PostAdmin(admin.ModelAdmin):
    inlines = (TagInline,)
    search_fields = (
        'name',
    )

    readonly_fields = (
        'subclass_type',
    )


@admin.register(Song)
class SongAdmin(PostAdmin):
    list_display = (
        'name',
        'user',
        'created_date',
        'genre',
    )


@admin.register(Poem)
class PoemAdmin(PostAdmin):
    list_display = (
        'name',
        'user',
        'created_date',
    )


admin.site.register(Genre)
