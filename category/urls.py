from django.contrib import admin
from django.urls import path, include
from category import views

urlpatterns = [
    path('', views.ListCreateCategoryView.as_view(),),
    path('/<slug:category_slug>/', views.UpdateDeleteCategoryView.as_view()),

]