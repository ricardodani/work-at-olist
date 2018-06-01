import json
from pygments import highlight
from pygments.lexers import JsonLexer
from pygments.formatters import HtmlFormatter
from django.contrib import messages
from django.contrib import admin
from django.utils.safestring import mark_safe
from bills.models import Bill


class BillAdmin(admin.ModelAdmin):
    search_fields = ['source']
    list_filter = ['created_at', 'updated_at', 'period']
    list_display = ['__str__', 'source', 'period', 'created_at', 'updated_at']
    fields = ['source', 'period', 'pretty_metadata']
    readonly_fields = ['pretty_metadata']
    actions = ['update_metadata']

    def pretty_metadata(self, bill):
        response = json.dumps(bill.metadata, indent=2)
        formatter = HtmlFormatter(style='colorful')
        response = highlight(response, JsonLexer(), formatter)
        style = "<style>{}</style>".format(formatter.get_style_defs())
        return mark_safe(style + response)
    pretty_metadata.short_description = 'Metadata'

    def update_metadata(self, request, queryset):
        try:
            for bill in queryset:
                bill.update_metadata()
            self.message_user(request, 'Updated metadata of selected bill`s.')
        except Exception as e:
            self.message_user(
                request, 'Could not update bill`s metadata.',
                level=messages.ERROR
            )
    update_metadata.short_description = 'Update metadata'


admin.site.register(Bill, BillAdmin)
