from django.contrib import admin
from django.urls import include, path
from . import views

urlpatterns = [
    path('<str:username>', views.cart, name='cart'),
    # path('add_cart/<slug:product_slug>/<str:username>/', views.add_cart, name='add_cart'),
    # path('reduce_cart/<slug:product_slug>/<str:username>/', views.reduce_cart, name='reduce_cart'),
    # path('remove_cart_item/<slug:product_slug>/<str:username>/', views.remove_cart_item, name='remove_cart_item'),
    path('add_cart/<slug:product_slug>/', views.add_cart, name='add_cart'),
    path('reduce_cart/<slug:product_slug>', views.reduce_cart, name='reduce_cart'),
    path('remove_cart_item/<slug:product_slug>', views.remove_cart_item, name='remove_cart_item'),
]