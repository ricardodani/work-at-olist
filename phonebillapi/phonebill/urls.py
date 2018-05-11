from django.urls import path

from phonebill import views

urlpatterns = [
    path('add-record/', views.CallRecordCreateView.as_view()),
    path('get-bill/', views.BillRetrieveView.as_view()),
]
