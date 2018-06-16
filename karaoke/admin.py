from django.contrib import admin

from analytics.models import TagPost
from karaoke.models import Song, Genre, Poem, Post, Karaoke
from musikhar.utils import conn


class TagInline(admin.TabularInline):
    model = TagPost
    extra = 1


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('name', 'subclass_type', 'last_time_updated', 'popularity_rate', 'popularity')
    inlines = (TagInline,)
    list_filter = ('subclass_type',)
    search_fields = (
        'name',
    )

    actions = ('clear_popular_cache', 'clear_news_cache', 'clear_free_cache')

    def clear_popular_cache(self, request, queryset):
        for pattern in conn().keys('/song/posts/popular/*'):
            conn().delete(pattern)

    def clear_news_cache(self, request, queryset):
        for pattern in conn().keys('/song/posts/news/*'):
            conn().delete(pattern)

    def clear_free_cache(self, request, queryset):
        for pattern in conn().keys('/song/posts/free/*'):
            conn().delete(pattern)


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name', 'count')
    actions = ('clear_cache',)

    def clear_cache(self, request, queryset):
        for genre in queryset:
            cache_str = '/song/genre/{}/karaokes/*'.format(genre.id)
            for pattern in conn().keys(cache_str):
                conn().delete(pattern)
        return

    def count(self, obj):
        return obj.post_set.filter(subclass_type=Post.KARAOKE_TYPE).count()


# admin.site.register(Genre)
admin.site.register(Song)
admin.site.register(Karaoke)
admin.site.register(Poem)
