from django.conf import settings
from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('', include('site_index.urls')),
    path('bills/', include('bills.urls')),
    path('call-records/', include('call_records.urls')),
    path('admin/', admin.site.urls),
]

# django-debug-toolbar
if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__', include(debug_toolbar.urls))
    ] + urlpatterns

admin.site.site_title = admin.site.site_header = 'PhoneBillAPI Admin'
