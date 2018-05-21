from django.urls import path
from call_records.views import CallRecordView


urlpatterns = [
    path('add/', CallRecordView.as_view(), name="add-record"),
]
