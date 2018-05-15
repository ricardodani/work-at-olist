from django.urls import path

from phonebill import views

urlpatterns = [
    path('add-record/', views.CallRecordCreateView.as_view()),
    path('get-bill/<slug:source>/', views.BillRetrieveView.as_view()),
]
