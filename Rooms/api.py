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


    return JsonResponse({'playerID':player.id, "currentRoom": player.current_room},safe=True)

@api_view(["GET"])
def worldmap(request):

    return JsonResponse(roomController.toDict(),safe=True)
