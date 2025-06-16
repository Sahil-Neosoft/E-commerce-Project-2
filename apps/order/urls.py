from django.urls import path
from .views import buy_now  #order_create, order_detail, order_list, order_cancel

urlpatterns = [
    # path('', order_list, name='order_list'),
    # path('create/', order_create, name='order_create'),
    # path('<int:pk>/', order_detail, name='order_detail'),
    # path('<int:pk>/cancel/', order_cancel, name='order_cancel'),
    path('', buy_now, name='buy_now'),
]