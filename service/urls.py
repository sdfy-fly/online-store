from django.urls import path 
from django.contrib.auth import views as auth_views

from .views import *


urlpatterns = [
    path('', index , name='home') ,
    path('item/<int:id>', getItem , name='item') ,
    path('buy/<int:id>', create_checkout_session , name='buy') ,
    
    path('success', successPaymernt , name='success') ,
    path('failed', failedPaymernt , name='success') ,
    path('order' , getOrder , name='order'),
    
    path('register' , register , name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='service/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    path('addItemToOrder/<int:id>', addItemToOrder, name='addItemToOrder'),
    path('clear-order' , clearOrder , name='clear-order'),
    path('paymentOrder' , paymentOrder , name='payment-order'),
]