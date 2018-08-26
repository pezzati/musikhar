from django.contrib import admin
from rangefilter.filter import DateTimeRangeFilter

from loginapp.models import User, Token, Follow, Artist, Verification, Device

admin.site.register(Artist)


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = (
        'follower',
        'followed'
    )

    readonly_fields = (
        'follower',
        'followed'
    )


@admin.register(Token)
class TokenAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'key',
        'created'
    )

    readonly_fields = (
        'user',
        'key',
        'created'
    )


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    search_fields = ('username', 'mobile', 'email')
    list_display = ('username', 'mobile', 'email', 'date_joined')
    filter_horizontal = ('genres', 'user_permissions', 'groups')
    list_filter = ('is_premium', ('date_joined', DateTimeRangeFilter))

    def save_model(self, request, obj, form, change):
        if not obj.id or User.objects.get(id=obj.id).password != obj.password:
            obj.set_password(obj.password)

        super(UserAdmin, self).save_model(request, obj, form, change)


class DeviceUserMode(admin.SimpleListFilter):
    title = 'User State'
    parameter_name = 'view_mood'
    default_value = 'none'
    has_user = 'exists'

    def lookups(self, request, model_admin):
        return [('none', 'None'),
                ('exists', 'Has User')]

    def queryset(self, request, queryset):
        if self.value() == 'all':
            return queryset
        elif self.value() == self.has_user:
            return queryset.filter(user__isnull=False)
        else:
            return queryset.filter(user__isnull=True)

    def value(self):
        value = super(DeviceUserMode, self).value()
        if value is None:
            value = self.default_value
        return value


@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = ('user', 'last_update_date', 'udid', 'one_signal_id')
    search_fields = ('user__username', )
    list_filter = ('type', ('last_update_date', DateTimeRangeFilter), DeviceUserMode)

    def get_readonly_fields(self, request, obj=None):
        if obj:
            self.readonly_fields = [field.name for field in obj.__class__._meta.fields]
        return self.readonly_fields


admin.site.register(Verification)


