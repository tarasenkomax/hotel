from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from Room.models import Room, Reserve
from Room.reserve_functions import check_availability, number_of_days, dates_of_user


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


def help_page(request):
    """ Информация по отдельной комнате """
    return render(request, 'rooms/help_page.html', )


def all_reserves(request):
    """ Вывод всех броней пользователя"""
    reserve_list = Reserve.objects.filter(client=request.user).order_by('-id')
    paginator = Paginator(reserve_list, 3)  # 3 поста на каждой странице
    page = request.GET.get('page')
    try:
        reserves = paginator.page(page)
    except PageNotAnInteger:
        # Если страница не является целым числом, поставим первую страницу
        reserves = paginator.page(1)
    except EmptyPage:
        # Если страница больше максимальной, доставить последнюю страницу результатов
        reserves = paginator.page(paginator.num_pages)
    return render(request, 'rooms/all_reserves.html', {'page': page, 'reserves': reserves, })


def pay(request, number):
    """ Оплата брони (заглушка)"""
    if request.method == 'GET':
        full_price = request.GET['full_price']
        reserve = Reserve()
        reserve.day_in = request.GET['day_in']
        reserve.day_out = request.GET['day_out']
        reserve.room = get_object_or_404(Room, number=number)
        reserve.number_of_guests = request.GET['number_of_guests']
        reserve.client = request.user
        if check_availability(reserve.room, reserve.day_in, reserve.day_out):
            reserve.save()
            message = 'Номер успешно забронирован. Информацию о брони вы можете посмотреть в разделе "Мои резервы".'
        else:
            message = 'Ошибка оплаты.'
        return render(request, 'rooms/pay.html', {'message': message, })


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
        if dates_of_user(request.user, day_in, day_out):
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
        else:
            return redirect('help_page')
