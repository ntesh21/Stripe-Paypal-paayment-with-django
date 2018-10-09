# payments/urls.py
from django.urls import path, include

from . import views

urlpatterns = [
    path('charge/', views.charge, name='charge'),
    path('', views.HomePageView.as_view(), name='home'), 
    path('stripe/', views.PackagesView.as_view(), name='stripe'),
    path('paypal/', include('paypal.standard.ipn.urls')),
    path('paypal_pay/', views.paypal_pay, name='paypal_pay'),
    path('done/', views.pay_done, name='done'),
    path('canceled/', views.pay_canceled, name='canceled'),
    ]