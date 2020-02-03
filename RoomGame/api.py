from rest_framework import serializers, viewsets
from .models import PersonalNote

class PlayerSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Player
        fields = ('user_name', 'score', 'player_avatar', 'current_room')

class PlayerViewSet(viewsets.ModelViewSet):
    serializer_class = PlayerSerializer
    queryset = Player.objects.all()
