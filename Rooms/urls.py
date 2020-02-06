from django.conf.urls import url
from . import api

urlpatterns=[
    url('init', api.initialize),
    url('worldmap',api.worldmap),
    url('movetoroom',api.moveToRoom),
    url('playerinfo',api.playerinfo)
]

