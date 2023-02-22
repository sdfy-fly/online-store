from django.urls import path 

from .views import index, getItem, create_checkout_session, successPaymernt , failedPaymernt


urlpatterns = [
    path('', index , name='home') ,
    path('item/<int:id>', getItem , name='item') ,
    path('buy/<int:id>', create_checkout_session , name='buy') ,
    path('success', successPaymernt , name='success') ,
    path('failed', failedPaymernt , name='success') ,
    # path('api/get-cards', UserCards.as_view() , name='getCards') ,
]