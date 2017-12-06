from django.contrib import admin

from analytics.models import TagPost
from karaoke.models import Song, Genre, Poem, Post, Karaoke


class TagInline(admin.TabularInline):
    model = TagPost
    extra = 1


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    inlines = (TagInline,)
    search_fields = (
        'name',
    )


# @admin.register(Song)
# class SongAdmin(PostAdmin):
#     list_display = (
#         'name',
#         'user',
#         'created_date',
#         'genre',
#     )
#
#     readonly_fields = ('duration',)


@admin.register(Poem)
class PoemAdmin(PostAdmin):
    list_display = (
        'name',
        'user',
        'created_date',
    )


admin.site.register(Genre)
admin.site.register(Song)
admin.site.register(Karaoke)
