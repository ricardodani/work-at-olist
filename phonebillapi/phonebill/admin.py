from django.contrib import admin
from phonebill.models import Call, CallEnd, CallStart


class CallAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'source', 'destination', 'started_at', 'ended_at', 'price',
        'is_completed'
    ]
    search_fields = ['start_record__source']
    list_filter = ['start_record__timestamp', 'end_record__timestamp']
    readonly_fields = ['price']


admin.site.register(Call, CallAdmin)
admin.site.register(CallStart)
admin.site.register(CallEnd)
