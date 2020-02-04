from django.urls import path

from . import consumers

websocket_urlpatterns = [
    # re_path(r'ws/room/(?P<room_name>\w+)/$', consumers.RoomConsumer)
    path(r'ws/rooms/', consumers.RoomConsumer)
]
