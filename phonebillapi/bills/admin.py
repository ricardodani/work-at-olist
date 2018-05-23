from django.contrib import admin
from bills.models import Bill


class BillAdmin(admin.ModelAdmin):
    pass


admin.site.register(Bill, BillAdmin)
