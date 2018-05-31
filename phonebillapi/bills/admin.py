from django.contrib import admin
from bills.models import Bill


class BillAdmin(admin.ModelAdmin):
    search_fields = ['source']
    list_filter = ['created_at', 'updated_at', 'period']
    list_display = ['__str__', 'source', 'period']


admin.site.register(Bill, BillAdmin)
