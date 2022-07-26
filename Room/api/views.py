from rest_framework import generics, permissions
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated

from Room.api.serializers import AllRoomSerializer, RoomDetailSerializer, AllReservesSerializer
from Room.models import Room, Reserve


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


class AllReservesView(generics.ListAPIView):
    """
    Перечень всех броней пользователя (GET)
    """
    serializer_class = AllReservesSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Reserve.objects.filter(client=self.request.user).order_by('-id').select_related('review')

