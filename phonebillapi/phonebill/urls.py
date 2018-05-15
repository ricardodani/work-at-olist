from django.urls import path

from phonebill import views

urlpatterns = [
    path('', views.index, name="index"),
    path('add-record/', views.CallRecordCreateView.as_view(), name="add-record"),
    path('get-bill/', views.BillRetrieveView.as_view(), name="get-bill"),
]
