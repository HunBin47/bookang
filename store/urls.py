from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from . import views

urlpatterns = [
    path('', views.ListProductView.as_view()),
    path('/category/<slug:slug>/', views.ListProductView.as_view(),name='products_by_category'),
    path('/<slug:product_slug>/',views.ProductDetailView.as_view(lookup_field='product_slug')),
    path('/add', views.create_product, name='add_product'),
    path('/search/', views.search, name='search')
]