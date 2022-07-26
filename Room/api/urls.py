from django.urls import path

from Room.api.views import AllRoomsView, DetailRoomView

urlpatterns = [
    path('all_rooms', AllRoomsView.as_view(), name='api_all_rooms'),
    path('room/<int:number>', DetailRoomView.as_view(), name='api_detail_room'),
]
