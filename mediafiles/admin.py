from django.contrib import admin
from rangefilter.filter import DateTimeRangeFilter

from mediafiles.models import MediaFile, AsyncTask
from mediafiles.tasks import create_karaokes


@admin.register(MediaFile)
class MediaFileAdmin(admin.ModelAdmin):
    list_display = ('path', 'created_date', 'resource_type', 'type')
    list_filter = ('resource_type', 'type', ('created_date', DateTimeRangeFilter))


@admin.register(AsyncTask)
class AsyncTaskAdmin(admin.ModelAdmin):
    list_display = ('name', 'state', 'type', 'creation_date')
    list_editable = ('state',)
    actions = ['process_it']

    def process_it(self, request, queryset):
        for obj in queryset:
            if obj.state == AsyncTask.STATE_ADDED:
                create_karaokes.delay(obj.id)
    process_it.short_description = 'Process Tasks'
