from django.contrib import admin

from financial.models import BusinessPackage, UserPaymentTransaction


@admin.register(BusinessPackage)
class BusinessPackageAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'years', 'months', 'weeks', 'days', 'active')
    list_editable = ('active',)
    readonly_fields = ('serial_number',)


@admin.register(UserPaymentTransaction)
class UserPaymentTransactionAdmin(admin.ModelAdmin):
    list_display = ('user', 'date', 'amount', 'days')
    readonly_fields = ('user', 'date', 'amount', 'days', 'applied')
    search_fields = ('user__username', 'days', 'amount')

