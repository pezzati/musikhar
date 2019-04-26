from datetime import datetime

from django.contrib import admin
from rangefilter.filter import DateTimeRangeFilter

from analytics.models import Favorite, Like, Banner, Tag, TagPost, UserFileHistory, Event, UserAction
from karaoke.models import Post
from mediafiles.models import AsyncTask
from mediafiles.tasks import generate_report

admin.site.register(Like)
admin.site.register(Favorite)
admin.site.register(Tag)
admin.site.register(TagPost)


@admin.register(UserFileHistory)
class UserFileHistoryAdmin(admin.ModelAdmin):
    readonly_fields = (
        'requested_user',
        'post',
        'date',
        'owner_user',
        'file_path'
    )
    list_display = (
        'user',
        'post',
        'date',
        'size'
    )

    def size(self, obj):
        try:
            return obj.post.get_file().file.size / 1000000
        except:
            return ''

    def user(self, obj):
        if obj.requested_user:
            return obj.requested_user
        else:
            return 'Anonymous'


@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'index',
        'is_active',
        'start_time',
        'end_time',
        'clicked_count',
        'link'
    )

    list_editable = (
        'is_active',
        'index'
    )

    readonly_fields = ('clicked_count',)


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = (
        'owner',
        'type',
        'creation_date',
        'user',
        'post'
    )
    readonly_fields = (
        'owner',
        'type',
        'creation_date',
        'user',
        'post'
    )

    list_filter = ('type',)


class TimestampDateTimeRangeFilter(DateTimeRangeFilter):
    def _make_query_filter(self, request, validated_data):
        query_params = super(TimestampDateTimeRangeFilter, self)._make_query_filter(request, validated_data)
        if query_params.get(self.lookup_kwarg_gte):
            query_params[self.lookup_kwarg_gte] = int(query_params.get(self.lookup_kwarg_gte).timestamp())
        if query_params.get(self.lookup_kwarg_lte):
            query_params[self.lookup_kwarg_lte] = int(query_params.get(self.lookup_kwarg_lte).timestamp())
        return query_params


@admin.register(UserAction)
class UserActionAdmin(admin.ModelAdmin):
    list_display = (
        'datetime',
        'user',
        'action',
        'detail_h',
        'session',
        'platform'
    )

    search_fields = ('user__username', '=detail', '=session')
    list_filter = (('timestamp', TimestampDateTimeRangeFilter), 'action', 'platform')
    actions = ('get_report',)

    def detail_h(self, obj):
        if obj.action == 'Karaoke Tapped':
            try:
                post = Post.objects.get(id=obj.detail)
                return '{} - {}'.format(post.name, post.genre.name)
            except:
                pass
        return obj.detail

    def get_report(self, request, queryset):
        task = AsyncTask.objects.create(name='UserAction_{}'.format(datetime.now().strftime('%H-%M')),
                                        type=AsyncTask.GET_REPORT,
                                        creation_date=datetime.now())
        generate_report.delay(task.id)
        return

    # def get_queryparams(self, request):
    #     querystring = request.GET
    #     if not querystring:
    #         return {}
    #     query_params = {}
    #     for key in querystring:
    #         if 'timestamp' in key:
    #             continue
    #         query_params[key] = querystring.get(key)
    #
    #     print(query_params)


