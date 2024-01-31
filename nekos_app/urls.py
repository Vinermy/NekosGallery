from django.urls import path

from nekos_app import views

urlpatterns = [
    path('index', views.index, name='index')
]