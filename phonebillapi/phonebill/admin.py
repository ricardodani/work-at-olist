from django.contrib import admin
from phonebill.models import Call


class CallAdmin(admin.ModelAdmin):
    pass


admin.site.register(Call, CallAdmin)
