from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('phonebill.urls')),
]

admin.site.site_title = admin.site.site_header = 'Phone Bill Admin'
