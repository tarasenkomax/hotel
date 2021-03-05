from django.contrib import admin
from django.utils.safestring import mark_safe

from Room.models import Hotel, Room, TypeRoom, Gallery, Reserve


class HotelAdmin(admin.ModelAdmin):
    """ Отели """
    list_display = ('name',)
    list_display_links = ('name',)


class GalleryInLine(admin.StackedInline):
    model = Gallery
    extra = 1


class RoomAdmin(admin.ModelAdmin):
    """ Команты """
    list_display = ('number', 'type', 'price', 'number_of_guests',)
    list_display_links = ('number',)
    search_fields = ('number',)
    list_filter = ('type', 'number_of_guests',)

    inlines = [GalleryInLine]


class TypeRoomAdmin(admin.ModelAdmin):
    """ Типы комнат"""
    list_display = ('nomination',)
    list_display_links = ('nomination',)


class GalleryAdmin(admin.ModelAdmin):
    """ Фотографии комнат """
    list_display = ('room',)
    list_display_links = ('room',)


class ReserveAdmin(admin.ModelAdmin):
    """ Резервы комнат """
    list_display = ('id', 'room', 'client', 'day_in', 'day_out', 'number_of_guests')
    list_display_links = ('room',)
    list_filter = ('room',)


admin.site.register(Reserve, ReserveAdmin)
admin.site.register(Hotel, HotelAdmin)
admin.site.register(Room, RoomAdmin)
admin.site.register(TypeRoom, TypeRoomAdmin)
admin.site.register(Gallery, GalleryAdmin)

admin.site.site_title = 'Панель Админимтратора Отеля'
admin.site.site_header = 'Панель Администратора Отеля'
