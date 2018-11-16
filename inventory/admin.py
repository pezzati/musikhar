from django.contrib import admin

from inventory.models import Inventory, PostProperty


@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
    list_display = ('user',)


@admin.register(PostProperty)
class PostPropertyAdmin(admin.ModelAdmin):
    list_display = ('post', 'inventory', 'count')


