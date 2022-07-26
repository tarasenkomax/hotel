from django.urls import path

from Room.api.views import AllRoomsView

urlpatterns = [
    path('all_rooms', AllRoomsView.as_view(), name='api_all_rooms'),
]
