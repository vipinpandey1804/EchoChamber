from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.db.models import Sum, Max
from .models import EchoGame, Echo, PowerUp, Leaderboard
from .serializers import (
    GameCreateSerializer, PlayerActionSerializer, GameCompleteSerializer,
    EchoGameSerializer, LeaderboardSerializer
)
from .utils import (
    generate_maze, get_maze_size, spawn_power_ups, spawn_mines,
    spawn_score_powerups, generate_movable_walls, generate_echo_personality,
    calculate_echo_position, calculate_score
)
import random

class CreateGameAPIView(APIView):
    def post(self, request):
        serializer = GameCreateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        data = serializer.validated_data
        level = data['level']
        size = get_maze_size(level)
        
        # Get current score from request or use starting score for level 1
        current_score = data.get('current_score', getattr(settings, 'GAME_STARTING_SCORE', 100))
        if level == 1:
            current_score = getattr(settings, 'GAME_STARTING_SCORE', 100)
        
        try:
            maze = generate_maze(size, size, level)
            power_ups = spawn_power_ups(size, size, maze)
            mines = spawn_mines(size, size, maze, level)
            score_ups = spawn_score_powerups(size, size, maze, level)
            
            game = EchoGame.objects.create(
                player_id=data['player_id'],
                maze_data=maze,
                player_pos=[1, 1],
                level=level,
                score=current_score
            )
            
            for pu in power_ups:
                PowerUp.objects.create(
                    game=game,
                    power_type=pu['type'],
                    position=pu['pos'],
                    spawn_time=0,
                    expire_time=pu['expire']
                )
            
            movable_walls = []
            if level >= 6:
                movable_walls = generate_movable_walls(size, size, maze, level)
            
            return Response({
                'game_id': game.id,
                'maze': maze,
                'player_pos': [1, 1],
                'level': level,
                'power_ups': power_ups,
                'mines': mines,
                'score_ups': score_ups,
                'movable_walls': movable_walls,
                'current_score': current_score
            }, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            return Response(
                {'error': str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class PlayerActionAPIView(APIView):
    def post(self, request, game_id):
        serializer = PlayerActionSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        game = get_object_or_404(EchoGame, id=game_id)
        data = serializer.validated_data
        
        # Start with current score from database
        current_score = game.score if game.score > 0 else getattr(settings, 'GAME_STARTING_SCORE', 100)
        
        # Handle wall hits
        if data['wall_hit']:
            game.wall_hits += 1
            wall_penalty = getattr(settings, 'GAME_WALL_HIT_PENALTY', 10)
            current_score -= wall_penalty
        
        # Handle special actions
        if data['action'] == 'mine_hit':
            mine_penalty = getattr(settings, 'GAME_MINE_PENALTY', 50)
            current_score -= mine_penalty
        elif data['action'] == 'collect_score':
            coin_bonus = getattr(settings, 'GAME_COIN_BONUS', 25)
            current_score += coin_bonus
        
        # Handle powerup collection
        collected_powerup = None
        for pu in game.powerup_set.filter(collected=False):
            if (pu.position == data['position'] and 
                data['game_tick'] < pu.expire_time):
                pu.collected = True
                pu.save()
                collected_powerup = pu.power_type
                powerup_bonus = getattr(settings, 'GAME_POWERUP_BONUS', 50)
                current_score += powerup_bonus
                break
        
        # Create echo only for speak action
        if data['action'] == 'speak':
            personality = generate_echo_personality(data['action'], game.player_pos)
            maze_data = game.maze_data
            maze_height = len(maze_data)
            maze_width = len(maze_data[0]) if maze_data else 15
            echo_pos = calculate_echo_position(
                game.player_pos, data['position'], personality, maze_width, maze_height
            )
            
            Echo.objects.create(
                game=game,
                action_type=data['action'],
                original_pos=game.player_pos,
                echo_pos=echo_pos,
                personality=personality,
                replay_time=game.echo_set.count() + random.randint(3, 8)
            )
            
            # Echo penalty
            echo_penalty = getattr(settings, 'GAME_ECHO_PENALTY', 2)
            current_score -= echo_penalty
        
        # Ensure score doesn't go below 0
        current_score = max(0, current_score)
        
        game.player_pos = data['position']
        game.score = current_score
        game.save()
        
        return Response({
            'success': True,
            'echoes': list(game.echo_set.values()),
            'collected_powerup': collected_powerup,
            'wall_hits': game.wall_hits,
            'current_score': current_score
        })

class CompleteGameAPIView(APIView):
    def post(self, request, game_id):
        serializer = GameCompleteSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        game = get_object_or_404(EchoGame, id=game_id)
        data = serializer.validated_data
        
        echoes_used = game.echo_set.count()
        score = calculate_score(data['ticks'], echoes_used, game.wall_hits)
        
        game.score = score
        game.completed_at = timezone.now()
        game.save()
        
        Leaderboard.objects.create(
            player_id=game.player_id,
            level=game.level,
            score=score,
            completion_time=data['ticks']
        )
        
        return Response({
            'score': score,
            'ticks': data['ticks'],
            'echoes': echoes_used,
            'wall_hits': game.wall_hits
        })

class LeaderboardAPIView(APIView):
    def get(self, request):
        leaderboard = Leaderboard.objects.values('player_id').annotate(
            total_score=Sum('score'),
            max_level=Max('level')
        ).order_by('-total_score')[:10]
        
        return Response({'leaderboard': list(leaderboard)})
