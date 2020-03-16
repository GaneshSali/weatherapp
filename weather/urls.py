from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.main, name='weather'),
    path('delete/<str:city>', views.delete_city, name='delete_city')
]
