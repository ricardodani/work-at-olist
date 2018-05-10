from django.contrib import admin
from django.urls import path
import phonebill.urls

urlpatterns = [
    path('api/', phonebill.urls),
    path('admin/', admin.site.urls),
]

admin.site.site_title = admin.site.site_header = 'Phone Bill Admin'
