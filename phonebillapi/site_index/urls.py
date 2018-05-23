from django.urls import path
from site_index.views import index


app_name = 'site_index'
urlpatterns = [
    path('', index, name="index"),
]
