from django.urls import re_path, path

from . import consumers

websocket_urlpatterns = [
    # re_path(r'ws/room/(?P<room_name>\w+)/$', consumers.RoomConsumer)
    re_path(r'ws/rooms/(?P<playerID>[\w-]+)/?$', consumers.RoomConsumer),
    path('ws/rooms/', consumers.RoomConsumer)
]
