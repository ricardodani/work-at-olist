from django.contrib import admin
from bills.models import Bill


class BillAdmin(admin.ModelAdmin):
    list_display = ['id', 'source', 'period', 'total']
    search_fields = ['source']
    list_filter = ['created_at', 'updated_at']
    readonly_fields = ['calls', 'total', 'updated_at', 'created_at']


admin.site.register(Bill, BillAdmin)
