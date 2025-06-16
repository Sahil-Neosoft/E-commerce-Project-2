from django.urls import path
from .views import *
urlpatterns = [
    path('', cart_view, name='cart'),
    path('add/', add_to_cart, name='add_to_cart'),
    path('remove/', remove_from_cart, name='remove_from_cart'),
    path('increase/', increase_cart_item_quantity, name='increase_cart_item_quantity'),
    path('decrease/', decrease_cart_item_quantity, name='decrease_cart_item_quantity'),
]