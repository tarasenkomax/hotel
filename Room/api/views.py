from django.http import Http404
from rest_framework import generics, response, status
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from Room.api.serializers import AllRoomSerializer, RoomDetailSerializer, AllReservesSerializer, AddReviewSerializer
from Room.models import Room, Reserve, Review
from Room.utils import calculate_refund_amount


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


class CancelView(generics.RetrieveDestroyAPIView):
    """
    Получение информации по отмене брони (GET)
    Отмена брони (DEL)
    """
    queryset = Reserve.objects.all()
    lookup_field = 'pk'

    def get_object(self):
        reserve = Reserve.objects.select_related('client', 'room').get(pk=self.kwargs.get("pk"))
        if not reserve.client == self.request.user:
            raise Http404
        return reserve

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)
        return response.Response(data={'message': f'Успешно удалено'}, status=status.HTTP_204_NO_CONTENT)

    def get(self, request, *args, **kwargs):
        cancel_data = calculate_refund_amount(self.get_object())
        if cancel_data['delay']:
            return response.Response(data={'message': f'За отмену брони деньги вам не вернутся'})
        else:
            return response.Response(data={
                'message': f"""Вам вернется стоимость за {cancel_data['days']} дней с {self.get_object().day_in} по {self.get_object().day_out} в размере {cancel_data['cost']} рублей."""})


class AddReviewView(generics.CreateAPIView):
    """
    Добавление отзыва (POST)
    """
    serializer_class = AddReviewSerializer

    def get_object(self):
        reserve = get_object_or_404(Reserve, pk=self.kwargs["pk"])
        if not reserve.client == self.request.user:
            raise Http404
        if len(Review.objects.filter(reserve=reserve)) > 0:
            raise Http404
        return reserve

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        Review.objects.create(room=self.get_object().room,
                              rating=serializer.data['rating'],
                              body=serializer.data['body'],
                              author=self.request.user,
                              reserve=self.get_object())
        return Response(serializer.data, status=status.HTTP_201_CREATED)
