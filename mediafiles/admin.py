from django.contrib import admin

from mediafiles.models import MediaFile, AsyncTask
from mediafiles.tasks import create_karaokes

admin.site.register(MediaFile)


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
