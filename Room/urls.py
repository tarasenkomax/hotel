from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from Room import views

urlpatterns = [
    # ----- Комнаты -----
    path('all_rooms', views.all_rooms, name='all_rooms'),
    path('room/<int:number>', views.detail_room, name='detail_room'),
    path('list_free_rooms', views.list_free_rooms, name='list_free_rooms'),
    path('reserve_room/<int:number>', views.reserve_room, name='reserve_room'),
    path('all_reserves', views.all_reserves, name='all_reserves'),
    path('pay/<int:number>', views.pay, name='pay'),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
