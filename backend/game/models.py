from django.db import models
import json

class EchoGame(models.Model):
    player_id = models.CharField(max_length=100)
    maze_data = models.JSONField(default=dict)
    player_pos = models.JSONField(default=lambda: [1, 1])
    echoes = models.JSONField(default=list)
    level = models.IntegerField(default=1)
    score = models.IntegerField(default=0)
    wall_hits = models.IntegerField(default=0)
    power_ups = models.JSONField(default=list)
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    
class Echo(models.Model):
    PERSONALITIES = [
        ('chaotic', 'Chaotic'),
        ('helpful', 'Helpful'),
        ('mirror', 'Mirror'),
        ('delayed', 'Delayed')
    ]
    
    game = models.ForeignKey(EchoGame, on_delete=models.CASCADE)
    action_type = models.CharField(max_length=20)  # 'move', 'jump', 'speak'
    original_pos = models.JSONField()
    echo_pos = models.JSONField()
    personality = models.CharField(max_length=20, choices=PERSONALITIES)
    replay_time = models.IntegerField()  # game tick when echo activates
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

class PowerUp(models.Model):
    TYPES = [
        ('speed', 'Speed Boost'),
        ('phase', 'Phase Shield'),
        ('freeze', 'Time Freeze'),
        ('vision', 'Echo Vision')
    ]
    
    game = models.ForeignKey(EchoGame, on_delete=models.CASCADE)
    power_type = models.CharField(max_length=20, choices=TYPES)
    position = models.JSONField()
    collected = models.BooleanField(default=False)
    spawn_time = models.IntegerField()
    expire_time = models.IntegerField()

class Leaderboard(models.Model):
    player_id = models.CharField(max_length=100)
    level = models.IntegerField()
    score = models.IntegerField()
    completion_time = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-score', 'completion_time']
