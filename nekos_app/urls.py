from django.urls import path, re_path

from nekos_app import views

urlpatterns = [
    path('index', views.index, name='index'),
    path('image/<int:id>', views.image, name='image'),
    path('random_girl', views.random_girl, name='random_girl'),
    path('character_arts/<int:id>', views.character_arts, name='character_arts'),
    path('artist_arts/<int:id>', views.artist_arts, name='artist_arts'),
    re_path(r'search/?', views.search, name='search')
]