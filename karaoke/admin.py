from django.contrib import admin

from karaoke.models import Karaoke, Line, Genre


@admin.register(Karaoke)
class KaraokeAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'created_date',
        'genre',
    )

    search_fields = (
        'name',
    )


admin.site.register(Line)
admin.site.register(Genre)
