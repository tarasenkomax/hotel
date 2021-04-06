from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from Room.forms import AddReview
from Room.models import Room, Reserve, Review, Regulations
from Room.reserve_functions import check_availability, number_of_days, dates_of_user, average_rating, send_email
import datetime as DT


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
    regulations_list = Regulations.objects.filter(type_room=room.type)
    review_list = Review.objects.filter(room=room).order_by('-pub_date')
    num_of_review = len(review_list)
    page = request.GET.get('page')

    return render(request, 'rooms/detail_room.html',
                  {'room': room, 'page': page, 'review_list': review_list,
                   'num_of_review': num_of_review, 'regulations_list': regulations_list})


def help_page(request):
    """ Информация по отдельной комнате """
    return render(request, 'rooms/help_page.html', )


@login_required(login_url="login")
def all_reserves(request):
    """ Вывод всех броней пользователя"""
    reserve_list = Reserve.objects.filter(client=request.user).order_by('id')
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


@login_required(login_url="login")
def pay(request, number):
    """ Оплата брони (заглушка)"""
    if request.method == 'GET':
        reserve = Reserve()
        reserve.day_in = request.GET['day_in']
        reserve.day_out = request.GET['day_out']
        reserve.room = get_object_or_404(Room, number=number)
        reserve.number_of_guests = request.GET['number_of_guests']
        reserve.client = request.user
        if dates_of_user(request.user, reserve.day_in, reserve.day_out):
            reserve.save()
            message = 'Номер успешно забронирован. Детали бронирования были отправлены вам на электронную почту. Так ' \
                      'же информацию о брони вы можете посмотреть в разделе "Мои резервы". '
            send_email(request.user.name, request.user.patronymic, reserve.room, reserve.day_in, reserve.day_out,
                       reserve.number_of_guests, request.user.email)
        else:
            message = 'Ошибка оплаты.'
        return render(request, 'rooms/pay.html', {'message': message, })


def reserve_room(request, number):
    """ Бронирование коматы  """
    room = get_object_or_404(Room, number=number)
    regulations_list = Regulations.objects.filter(type_room=room.type)
    review_list = Review.objects.filter(room=room).order_by('-pub_date')
    num_of_review = len(review_list)
    if request.method == 'GET':
        day_in = request.GET['day_in']
        day_out = request.GET['day_out']
        number_of_guests = request.GET['number_of_guests']
        days = number_of_days(day_in, day_out)
        full_price = room.price * days

    return render(request, 'rooms/reserve_room.html', {'room': room, 'day_in': day_in, 'day_out': day_out,
                                                       'number_of_guests': number_of_guests, 'full_price': full_price,
                                                       'days': days, 'review_list': review_list,
                                                       'num_of_review': num_of_review,
                                                       'regulations_list': regulations_list})


@login_required(login_url="login")  # TODO обрабатывать и не авторизоавнных пользователей
def list_free_rooms(request):
    """ Вывод свободных номеров """
    if request.method == 'GET':
        day_in = request.GET['day_in']
        day_out = request.GET['day_out']
        number_of_guests = request.GET['number_of_guests']
        filtered_rooms = Room.objects.filter(number_of_guests__gte=int(number_of_guests)).order_by('number')
    elif request.method == 'POST':
        if request.POST['day_in'] and request.POST['day_out'] or request.POST['number_of_guests']:
            day_in = request.POST['day_in']
            day_out = request.POST['day_out']
            number_of_guests = request.POST['number_of_guests']
            filtered_rooms = Room.objects.filter(number_of_guests__gte=int(number_of_guests)).order_by('number')
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


@login_required(login_url="login")
def add_review(request, pk):
    form = AddReview()
    reserve = Reserve.objects.get(pk=pk)
    room_reserve = reserve.room
    day_in = reserve.day_in
    day_out = reserve.day_out
    if not reserve.client == request.user:
        raise Http404
    if request.method == 'POST':
        form = AddReview(request.POST)
        if form.is_valid():
            review = Review()
            review.room = reserve.room
            review.author = request.user
            review.reserve = reserve
            review.rating = form.cleaned_data['rating']
            review.body = form.cleaned_data['body']
            review.pub_date = timezone.datetime.now()
            review.save()
            room_reserve.rating = average_rating(room_reserve)
            room_reserve.save()
            return redirect('all_reserves')
    return render(request, 'rooms/add_review.html',
                  {'reserve': reserve, 'form': form, 'room_reserve': room_reserve, 'day_in': day_in,
                   'day_out': day_out, })
