from django.contrib import admin
from django.urls import include, path
from . import views

urlpatterns = [
    path('<str:username>', views.cart, name='cart'),
    path('add_cart/<slug:product_slug>/', views.add_cart, name='add_cart'),
    path('remove_cart/<int:product_id>/', views.remove_cart, name='remove_cart'),
    path('remove_cart_item/<int:product_id>/', views.remove_cart_item, name='remove_cart_item'),
]