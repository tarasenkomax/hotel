from django.urls import path

from Room.api.views import AllRoomsView, DetailRoomView, AllReservesView, CancelView

urlpatterns = [
    path('all_rooms', AllRoomsView.as_view(), name='api_all_rooms'),
    path('room/<int:number>', DetailRoomView.as_view(), name='api_detail_room'),
    path('all_reserves', AllReservesView.as_view(), name='api_all_reserves'),
    # path('list_free_rooms', ListFreeRooms.as_view(), name='list_free_rooms'),
    # path('reserve_room/<int:number>', ReserveRoom.as_view(), name='reserve_room'),
    path('cancel/<int:pk>', CancelView.as_view(), name='api_cancel'),
    # path('pay/<int:number>', Pay.as_view(), name='pay'),
    # path('add_review/<int:pk>', AddReview.as_view(), name='add_review'),
]
