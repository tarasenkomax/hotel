from rest_framework import generics

from Room.api.serializers import RoomSerializer
from Room.models import Room


class AllRoomsView(generics.ListAPIView):
    """
    Перечень всех комнат (GET)
    """
    serializer_class = RoomSerializer
    queryset = Room.objects.all()
