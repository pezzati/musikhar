from django.contrib import admin

from karaoke.models import Karaoke, Genre, Poem


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

    readonly_fields = (
        'subclass_type',
    )


@admin.register(Poem)
class PoemAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'created_date',
    )

    search_fields = (
        'name',
    )

    readonly_fields = (
        'subclass_type',
    )

admin.site.register(Genre)
