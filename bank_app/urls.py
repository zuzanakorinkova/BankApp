from django.contrib import admin
from django.urls import path
from . import views

app_name = 'bank_app'

urlpatterns = [
    path('', views.index, name='index'),
    path('customer/', views.customer_index, name='customer'),
    path('customer_account_details/<account_pk>/', views.customer_account_details,
         name='customer_account_details'),
    path('customer_make_transfer/', views.customer_make_transfer,
         name="customer_make_transfer"),
    path('staff/', views.staff_index, name='staff'),
    path('staff_customer_details/<customer_pk>/', views.staff_customer_details,
         name='staff_customer_details')
]
