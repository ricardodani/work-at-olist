from django.contrib import admin
from call_records.models import Call, NotCompletedCall, CompletedCall


class CallAdmin(admin.ModelAdmin):
    list_display = (
        'call_id', 'started_at', 'ended_at', 'source', 'destination', 'price',
        'is_completed', 'created_at', 'updated_at'
    )


class NotCompletedCallAdmin(CallAdmin):
    pass


class CompletedCallAdmin(CallAdmin):
    pass


admin.site.register(Call, CallAdmin)
admin.site.register(NotCompletedCall, NotCompletedCallAdmin)
admin.site.register(CompletedCall, CompletedCallAdmin)
