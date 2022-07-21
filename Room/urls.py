from django.urls import path

from Room import views

urlpatterns = [
    path('all_rooms', views.AllRooms.as_view(), name='all_rooms'),
    path('room/<int:number>', views.DetailRoom.as_view(), name='detail_room'),
    path('all_reserves', views.AllReserves.as_view(), name='all_reserves'),
    path('list_free_rooms', views.ListFreeRooms.as_view(), name='list_free_rooms'),
    path('reserve_room/<int:number>', views.ReserveRoom.as_view(), name='reserve_room'),
    path('cancel/<int:pk>', views.Cancel.as_view(), name='cancel'),
    path('pay/<int:number>', views.Pay.as_view(), name='pay'),
    path('add_review/<int:pk>', views.AddReview.as_view(), name='add_review'),
]
