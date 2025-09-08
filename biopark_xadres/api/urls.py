# api/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='chess_index'),
    path('api/game/start/', views.start_game, name='start_game'),
    path('api/game/<str:game_id>/move/', views.make_move, name='make_move'),
    path('api/game/<str:game_id>/status/', views.game_status, name='game_status'),
]