from django.contrib import admin
from rangefilter.filter import DateTimeRangeFilter

from financial.models import BusinessPackage, UserPaymentTransaction, BankTransaction, CoinTransaction, \
    BazzarTransaction


@admin.register(BusinessPackage)
class BusinessPackageAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'years', 'months', 'weeks', 'days', 'active')
    list_editable = ('active',)
    # readonly_fields = ('serial_number',)


@admin.register(UserPaymentTransaction)
class UserPaymentTransactionAdmin(admin.ModelAdmin):
    list_filter = ('applied',)
    list_display = ('user', 'date', 'amount', 'days', 'applied')
    readonly_fields = ('user', 'date', 'amount', 'days', 'applied')
    search_fields = ('user__username', 'days', 'amount')


@admin.register(BankTransaction)
class BankTransactionAdmin(admin.ModelAdmin):
    list_filter = ('state', ('creation_date', DateTimeRangeFilter))
    list_display = ('user', 'authority', 'amount', 'state')


@admin.register(CoinTransaction)
class CoinTransactionAdmin(admin.ModelAdmin):
    list_display = ('user', 'coins', 'amount', 'applied')


@admin.register(BazzarTransaction)
class BazzarTransactionAdmin(admin.ModelAdmin):
    list_display = ('user', 'package', 'serial_number', 'ref_id', 'package_applied')
