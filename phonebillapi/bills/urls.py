from django.urls import re_path
from bills.views import BillRetrieveView


urlpatterns = [
    re_path(r'^(?P<source>[0-9]{10,11})/',
            BillRetrieveView.as_view(),
            name="get-bill"),
]
