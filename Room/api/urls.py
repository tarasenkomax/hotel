from django.urls import path

from Room.api.views import AllRoomsView, DetailRoomView, AllReservesView, CancelView, AddReviewView, ListFreeRoomsView

urlpatterns = [
    path('all_rooms', AllRoomsView.as_view(), name='api_all_rooms'),
    path('room/<int:number>', DetailRoomView.as_view(), name='api_detail_room'),
    path('all_reserves', AllReservesView.as_view(), name='api_all_reserves'),
    path('list_free_rooms', ListFreeRoomsView.as_view(), name='api_list_free_rooms'),
    path('cancel/<int:pk>', CancelView.as_view(), name='api_cancel'),
    path('add_review/<int:pk>', AddReviewView.as_view(), name='api_add_review'),
]
