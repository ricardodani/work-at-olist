from django.urls import path
from site_index.views import index


urlpatterns = [
    path('', index, name="index"),
]
