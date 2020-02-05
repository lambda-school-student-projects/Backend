from django.db import models
from uuid import uuid4
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from .bsvPosition import Position
import time


#if changing the model -
#https://github.com/LambdaSchool/Intro-Django/blob/master/guides/day2.md#migrations-with-new-fields
class Player(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    current_room = models.UUIDField(default=uuid4)
    score = models.IntegerField(default=0)
    player_avatar = models.IntegerField(default=0)
    roomXPos = models.FloatField(default=0)
    roomYPos = models.FloatField(default=0)

    def initialize(self):
        self.save()

    def getPosition(self):
        return Position(self.roomXPos, self.roomYPos)

    def setPosition(self, newPosition):
        self.roomXPos = newPosition.x
        self.roomYPos = newPosition.y

        try:
            self.lastSave
        except:
            self.lastSave = 0
        # only update database every few seconds
        if time.monotonic() > self.lastSave + 5:
            self.save()
            self.lastSave = time.monotonic()

    def setRoom(self, newRoomID):
        self.current_room = newRoomID
        self.save()

@receiver(post_save, sender=User)
def create_user_player(sender, instance, created=False, **kwargs):
    if created:
        Player.objects.create(user=instance)
        Token.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_player(sender, instance, **kwargs):
    instance.player.save()
