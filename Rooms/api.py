from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from rest_framework.decorators import api_view
from .RoomModel.RoomController import roomController
from livestream.consumers import consumerController

import json

@api_view(["GET"])
def initialize(request):
    if request.user.is_anonymous:
        return
    user = request.user
    player = user.player
    roomController.spawnPlayerInRoom(player, player.current_room)
    return JsonResponse({'playerID':player.id, "currentRoom": player.current_room}, safe=True)

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

    if fromDirection is not None:
        roomController.spawnPlayerInRoom(player, newRoomID, fromDirection)
        return JsonResponse({"currentRoom": player.current_room})
    else:
        return JsonResponse({"error": "That room isn't connected"})


@api_view(["GET"])
def worldmap(request):

    return JsonResponse(roomController.toDict(), safe=True)
