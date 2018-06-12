from django.urls import path
from call_records.views import CallRecordView, BillRetrieveView


app_name = 'call_records'
urlpatterns = [
    path('post-record/', CallRecordView.as_view(), name="post-record"),
    path('get-bill/', BillRetrieveView.as_view(), name="get-bill"),
]
