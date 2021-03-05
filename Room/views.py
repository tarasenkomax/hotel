from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, get_object_or_404
from django.views import generic
from Room.models import Room, Reserve
from Room.reserve_functions import check_availability, number_of_days


def all_rooms(request):
    """ Список всех существующих комнат с пагинацией"""
    rooms_list = Room.objects.all().order_by('number')
    paginator = Paginator(rooms_list, 3)  # 3 поста на каждой странице
    page = request.GET.get('page')
    try:
        rooms = paginator.page(page)
    except PageNotAnInteger:
        # Если страница не является целым числом, поставим первую страницу
        rooms = paginator.page(1)
    except EmptyPage:
        # Если страница больше максимальной, доставить последнюю страницу результатов
        rooms = paginator.page(paginator.num_pages)
    return render(request, 'rooms/all_rooms.html', {'page': page, 'rooms': rooms})


def detail_room(request, number):
    """ Информация по отдельной комнате """
    room = get_object_or_404(Room, number=number)
    return render(request, 'rooms/detail_room.html', {'room': room, })


def reserve_room(request, number):
    """ Бронирование коматы  """
    room = get_object_or_404(Room, number=number)
    if request.method == 'GET':
        day_in = request.GET['day_in']
        day_out = request.GET['day_out']
        number_of_guests = request.GET['number_of_guests']
        days = number_of_days(day_in, day_out)
        full_price = room.price * days

    return render(request, 'rooms/reserve_room.html', {'room': room, 'day_in': day_in, 'day_out': day_out,
                                                       'number_of_guests': number_of_guests, 'full_price': full_price,
                                                       'days': days})


def list_free_rooms(request):
    """ Вывод свободных номеров """
    if request.method == 'GET':
        day_in = request.GET['day_in']
        day_out = request.GET['day_out']
        number_of_guests = request.GET['number_of_guests']
        filtered_rooms = Room.objects.filter(number_of_guests__gte=int(number_of_guests))
        free_rooms = []
        for room in filtered_rooms:
            if check_availability(room, day_in, day_out):
                free_rooms.append(room)
        paginator = Paginator(free_rooms, 3)  # 3 поста на каждой странице
        page = request.GET.get('page')
        try:
            rooms = paginator.page(page)
        except PageNotAnInteger:
            # Если страница не является целым числом, поставим первую страницу
            rooms = paginator.page(1)
        except EmptyPage:
            # Если страница больше максимальной, доставить последнюю страницу результатов
            rooms = paginator.page(paginator.num_pages)
        return render(request, 'rooms/list_free_rooms.html',
                      {'page': page, 'rooms': rooms, 'day_in': day_in, 'day_out': day_out,
                       'number_of_guests': number_of_guests})
