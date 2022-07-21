from django.contrib import admin

from Room.models import Hotel, Room, Gallery, Reserve, TypeRoom, Review, Regulations


class HotelAdmin(admin.ModelAdmin):
    """ Отели """
    list_display = ('name',)
    list_display_links = ('name',)
    readonly_fields = ('created_at', 'updated_at')


class ReviewAdmin(admin.ModelAdmin):
    """ Отзывы """
    list_display = ('room', 'reserve', 'author', 'rating', 'body', 'pub_date')
    list_display_links = ('room',)
    list_filter = ('room',)
    readonly_fields = ('created_at', 'updated_at')


class GalleryInLine(admin.StackedInline):
    model = Gallery
    extra = 1


class RoomAdmin(admin.ModelAdmin):
    """ Команты """
    list_display = ('number', 'type', 'price', 'number_of_guests')
    list_display_links = ('number',)
    search_fields = ('number',)
    list_filter = ('number_of_guests', 'type',)
    readonly_fields = ('created_at', 'updated_at')

    inlines = [GalleryInLine]


class TypeRoomAdmin(admin.ModelAdmin):
    """ Типы комнат"""
    list_display = ('code', 'nomination', 'description',)
    list_display_links = ('code', 'nomination',)
    readonly_fields = ('created_at', 'updated_at')


class GalleryAdmin(admin.ModelAdmin):
    """ Фотографии комнат """
    list_display = ('room',)
    list_display_links = ('room',)
    readonly_fields = ('created_at', 'updated_at')


class ReserveAdmin(admin.ModelAdmin):
    """ Резервы комнат """
    list_display = ('id', 'reg_date', 'room', 'client', 'day_in', 'day_out', 'number_of_guests')
    list_display_links = ('id',)
    list_filter = ('room',)
    date_hierarchy = 'reg_date'
    readonly_fields = ('reg_date', 'created_at', 'updated_at')


class RegulationsAdmin(admin.ModelAdmin):
    """ Правила комнат """
    list_display = ('type_room', 'regulation',)
    list_display_links = ('type_room',)
    list_filter = ('type_room',)
    readonly_fields = ('created_at', 'updated_at')


admin.site.register(Reserve, ReserveAdmin)
admin.site.register(Hotel, HotelAdmin)
admin.site.register(Regulations, RegulationsAdmin)
admin.site.register(Room, RoomAdmin)
admin.site.register(TypeRoom, TypeRoomAdmin)
admin.site.register(Gallery, GalleryAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.site_title = 'Панель Администратора Отеля'
admin.site.site_header = 'Панель Администратора Отеля'
