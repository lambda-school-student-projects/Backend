from django.conf.urls import url
from . import api

urlpatterns=[
    url('init', api.initialize),
    url('worldmap',api.worldmap),
]

