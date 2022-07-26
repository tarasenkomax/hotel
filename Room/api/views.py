from rest_framework import generics
from rest_framework.generics import get_object_or_404

from Room.api.serializers import AllRoomSerializer, RoomDetailSerializer
from Room.models import Room


class AllRoomsView(generics.ListAPIView):
    """
    Перечень всех комнат (GET)
    """
    serializer_class = AllRoomSerializer
    queryset = Room.objects.all()


class DetailRoomView(generics.RetrieveAPIView):
    """
    Получить комнату по номеру (GET)
    """
    serializer_class = RoomDetailSerializer

    def get_object(self):
        return get_object_or_404(Room, number=self.kwargs["number"])
