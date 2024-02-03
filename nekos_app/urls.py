from django.urls import path

from nekos_app import views

urlpatterns = [
    path('index', views.index, name='index'),
    path('image/<int:id>', views.image, name='image'),
    path('random_girl', views.random_girl, name='random_girl'),
    path('character_arts/<int:id>', views.character_arts, name='character_arts'),
    path('artist_arts/<int:id>', views.artist_arts, name='artist_arts'),
    path('search', views.search, name='search'),
    path('search_results', views.search_results, name='search_results'),
    path('image_by_id/<int:id>', views.image_card_by_id, name='image_by_id')
]