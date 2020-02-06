from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from rest_framework.decorators import api_view
from .bsvRoomController import roomController
from livestream.consumers import consumerController
from .models import Player

import json

@api_view(["POST"])
def initialize(request):
    if request.user.is_anonymous:
        return
    user = request.user
    player = user.player
    data = json.loads(request.body)
    player_avatar = data["player_avatar"]
    player.player_avatar = player_avatar
    player.save()
    roomController.spawnPlayerInRoom(player, player.current_room)
    return JsonResponse({'playerID': player.id, "currentRoom": player.current_room, "spawnLocation": player.getPosition().toArray()})

@api_view(["POST"])
def moveToRoom(request):
    if request.user.is_anonymous:
        return
    user = request.user
    player = user.player
    data = json.loads(request.body)
    newRoomID = data['roomID']
    oldRoomID = str(player.current_room)
    newRoom = roomController.getRoom(newRoomID)
    if newRoom is None:
        return JsonResponse({"error": "That room doesn't exist"})
    oldRoom = roomController.getRoom(oldRoomID)
    fromDirection = newRoom.cardinalDirectionOfConnectedRoom(oldRoom)
    roomController.spawnPlayerInRoom(player, newRoomID, fromDirection)
    return JsonResponse({"currentRoom": player.current_room, "fromDirection": str(fromDirection), "spawnLocation": player.getPosition().toArray()})


@api_view(["GET"])
def worldmap(request):

    return JsonResponse(roomController.toDict(), safe=True)


@api_view(["POST"])
def playerinfo(request):
    if request.user.is_anonymous:
        return
    data = json.loads(request.body)
    requestedId = data["id"]
    requestedPlayer = Player.objects.get(id = requestedId)
    playerProperties = {"player_avatar":requestedPlayer.player_avatar, "username":requestedPlayer.user.username}
    return JsonResponse(playerProperties)

