from django.urls import path
from bills.views import BillRetrieveView


app_name = 'bills'
urlpatterns = [
    path(r'get/', BillRetrieveView.as_view(), name="get-bill"),
]
