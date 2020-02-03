from django.db import models
from uuid import uuid4

#if changing the model -
#https://github.com/LambdaSchool/Intro-Django/blob/master/guides/day2.md#migrations-with-new-fields
class Player(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    user_name = models.CharField(max_length=30, unique=True)
    user_pass = models.CharField(max_length=30)
    current_room = models.CharField(max_length=30)
    score = models.IntegerField(default=0)
    player_avatar = models.IntegerField(default=0)

