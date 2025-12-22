from django.urls import path
from .views import (
    CreateGameAPIView, PlayerActionAPIView, 
    CompleteGameAPIView, LeaderboardAPIView
)

urlpatterns = [
    path('create/', CreateGameAPIView.as_view(), name='create_game'),
    path('<int:game_id>/action/', PlayerActionAPIView.as_view(), name='player_action'),
    path('<int:game_id>/complete/', CompleteGameAPIView.as_view(), name='complete_game'),
    path('leaderboard/', LeaderboardAPIView.as_view(), name='leaderboard'),
]