from django.urls import path

from nekos_app import views

urlpatterns = [
    path('index', views.index, name='index'),
    path('image/{id:int}', views.image, name='image'),
    path('random_girl', views.random_girl, name='random_girl')
]