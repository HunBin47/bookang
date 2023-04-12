from django.contrib import admin
from django.urls import path, include
from category import views

urlpatterns = [
    path('category/', views.ListCreateCategoryView.as_view(),),
    path('category/<int:pk>', views.UpdateDeleteCategoryView.as_view()),

]