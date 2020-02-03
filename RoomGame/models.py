from django.db import models

class Player(models.Model):
    user_name = models.CharField(max_length=30, unique=true)
    user_pass = models.CharField(max_length=30)
    current_room = models.CharField(max_length=30)
    score = models.IntegerField(default=0)
    player_avatar = models.IntegerField(default=0)
    