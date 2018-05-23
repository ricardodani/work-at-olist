from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('', include('site_index.urls')),
    path('bills/', include('bills.urls')),
    path('call-records/', include('call_records.urls')),
    path('admin/', admin.site.urls),
]


admin.site.site_title = admin.site.site_header = 'PhoneBillAPI Admin'
