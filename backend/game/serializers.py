from rest_framework import serializers
from .models import EchoGame, Echo, PowerUp, Leaderboard

class EchoGameSerializer(serializers.ModelSerializer):
    class Meta:
        model = EchoGame
        fields = '__all__'

class EchoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Echo
        fields = '__all__'

class PowerUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = PowerUp
        fields = '__all__'

class LeaderboardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Leaderboard
        fields = '__all__'

class GameCreateSerializer(serializers.Serializer):
    player_id = serializers.CharField(max_length=100, default='guest')
    level = serializers.IntegerField(default=1)
    current_score = serializers.IntegerField(required=False)

class PlayerActionSerializer(serializers.Serializer):
    action = serializers.CharField(max_length=20)
    position = serializers.ListField(child=serializers.IntegerField(), min_length=2, max_length=2)
    wall_hit = serializers.BooleanField(default=False)
    game_tick = serializers.IntegerField(default=0)

class GameCompleteSerializer(serializers.Serializer):
    ticks = serializers.IntegerField(default=0)