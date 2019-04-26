from django.contrib import admin
from rangefilter.filter import DateTimeRangeFilter

from financial.models import BusinessPackage, UserPaymentTransaction, BankTransaction, CoinTransaction, \
    BazzarTransaction, GiftCode, UserGiftCode


@admin.register(BusinessPackage)
class BusinessPackageAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'index', 'years', 'months', 'weeks', 'days', 'coins', 'active')
    list_editable = ('active', 'index')
    # readonly_fields = ('serial_number',)


@admin.register(UserPaymentTransaction)
class UserPaymentTransactionAdmin(admin.ModelAdmin):
    list_filter = ('applied', 'transaction_info')
    list_display = ('user', 'date', 'amount', 'days', 'applied')
    readonly_fields = ('user', 'date', 'amount', 'days', 'applied')
    search_fields = ('user__username', 'days', 'amount')


@admin.register(BankTransaction)
class BankTransactionAdmin(admin.ModelAdmin):
    list_filter = ('state', ('creation_date', DateTimeRangeFilter))
    list_display = ('user', 'authority', 'amount', 'state', 'creation_date')


@admin.register(CoinTransaction)
class CoinTransactionAdmin(admin.ModelAdmin):
    list_display = ('user', 'coins', 'amount', 'applied')
    list_filter = ('transaction_info',)


@admin.register(BazzarTransaction)
class BazzarTransactionAdmin(admin.ModelAdmin):
    list_display = ('user', 'package', 'serial_number', 'ref_id', 'package_applied')


@admin.register(GiftCode)
class GiftCodeAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'gift', 'active', 'capacity', 'deadline', 'used')
    list_editable = ('active', 'capacity', 'deadline')

    def used(self, obj):
        return obj.users.count()

    def get_form(self, request, obj=None, **kwargs):
        form = super(GiftCodeAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields['gift'].queryset = BusinessPackage.objects.filter(gifted=True)
        return form


@admin.register(UserGiftCode)
class UserGiftCodeAdmin(admin.ModelAdmin):
    list_display = ('user', 'gift_code', 'used_time', 'applied')



