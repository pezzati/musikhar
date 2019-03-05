from django.contrib import admin

from analytics.models import TagPost
from karaoke.models import Song, Genre, Poem, Post, Karaoke, Feed
from musikhar.utils import conn


class TagInline(admin.TabularInline):
    model = TagPost
    extra = 1


class KaraokeInline(admin.StackedInline):
    model = Karaoke


class SongInline(admin.StackedInline):
    model = Song


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):

    list_display = ('name', 'legal', 'price', 'count', 'is_premium', 'last_time_updated', 'popularity_rate', 'popularity')
    list_editable = ('is_premium', 'legal')
    inlines = (TagInline, KaraokeInline)
    list_filter = ('subclass_type', 'is_premium', 'genre')
    search_fields = (
        'name',
    )

    actions = ('clear_popular_cache', 'clear_news_cache', 'clear_free_cache',
               'clear_home_feed_cache',
               'clear_all_caches')

    def clear_popular_cache(self, request, queryset):
        for pattern in conn().keys('/song/posts/popular/*'):
            conn().delete(pattern)

    def clear_news_cache(self, request, queryset):
        for pattern in conn().keys('/song/posts/news/*'):
            conn().delete(pattern)

    def clear_free_cache(self, request, queryset):
        for pattern in conn().keys('/song/posts/free/*'):
            conn().delete(pattern)

    def clear_home_feed_cache(self, request, queryset):
        for pattern in conn().keys('home_feed*'):
            conn().delete(pattern)

    def clear_all_caches(self, request, queryset):
        for pattern in conn().keys('home_feed*'):
            conn().delete(pattern)

        for pattern in conn().keys('/song/posts/popular/*'):
            conn().delete(pattern)

        for pattern in conn().keys('/song/posts/news/*'):
            conn().delete(pattern)

        for pattern in conn().keys('/song/posts/free/*'):
            conn().delete(pattern)

        for pattern in conn().keys('/song/genre/*'):
            conn().delete(pattern)

        for pattern in conn().keys('/song/feed/*'):
            conn().delete(pattern)

    def get_inline_instances(self, request, obj=None):
        self.inlines = (TagInline, KaraokeInline)
        if obj.subclass_type == Post.SONG_TYPE:
            self.inlines = (TagInline, SongInline)
        return super(PostAdmin, self).get_inline_instances(request, obj=obj)


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name', 'count', 'index')
    list_editable = ('index',)
    actions = ('clear_cache', 'clear_all_genre_cache')

    def clear_cache(self, request, queryset):
        for genre in queryset:
            cache_str = '/song/genre/{}/karaokes/*'.format(genre.id)
            for pattern in conn().keys(cache_str):
                conn().delete(pattern)
        return

    def clear_all_genre_cache(self, request, queryset):
        for pattern in conn().keys('/song/genre/*'):
            conn().delete(pattern)

    def count(self, obj):
        return obj.post_set.filter(subclass_type=Post.KARAOKE_TYPE).count()


@admin.register(Karaoke)
class KaraokeAdmin(admin.ModelAdmin):
    list_display = ('post',)
    search_fields = ('name', 'artist__name')


@admin.register(Feed)
class FeedAdmin(admin.ModelAdmin):
    filter_horizontal = ('tags',)
    list_display = ('name', 'code')

    actions = ('clear_cache', 'clear_all_genre_cache')

    def clear_cache(self, request, queryset):
        for feed in queryset:
            cache_str = '/song/genre/{}/*'.format(feed.code)
            for pattern in conn().keys(cache_str):
                conn().delete(pattern)
        return

    def clear_all_genre_cache(self, request, queryset):
        for pattern in conn().keys('/song/feed/*'):
            conn().delete(pattern)


@admin.register(Song)
class SongAdmin(admin.ModelAdmin):
    list_display = ('post', 'karaoke', 'reviewed', 'verified', 'publish')
    list_editable = ('reviewed', 'verified', 'publish')
    search_fields = ('karaoke__post__name',)


admin.site.register(Poem)
