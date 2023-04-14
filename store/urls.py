from django.urls import path
from . import views

urlpatterns = [
    path('', views.ListCreateProductView.as_view(), name='store'),
    path('category/<slug:category_slug>/', views.ListCreateProductView.as_view(), name='products_by_category'),
    path('category/<slug:category_slug>/<slug:product_slug>/',views.ListCreateProductView.as_view(), name='product_detail'),
    # path('search/', views.search, name='search'),
    # path('submit_review/<int:product_id>/', views.submit_review, name='submit_review'),
]