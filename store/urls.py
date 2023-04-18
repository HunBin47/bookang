from django.urls import path
from . import views

urlpatterns = [
    path('', views.ListProductView.as_view(), name='store'),
    path('category/<slug:category_slug>/', views.ListProductView.as_view(), name='products_by_category'),
    path('category/<slug:category_slug>/<slug:product_slug>/',views.ListProductView.as_view(), name='product_detail'),
    # path('search/', views.search, name='search')
]