from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, DeleteView

from Room.forms import ReviewForm
from Room.models import Room, Reserve, Review, Regulations
from Room.utils import check_availability, get_number_of_days, check_dates_of_user, send_email, send_email_cancel, \
    convert_str_to_date
import datetime as DT


class AllRooms(ListView):
    """ Список всех существующих комнат """
    context_object_name = 'rooms'
    queryset = Room.objects.all().order_by('number').select_related('type', 'photos_of_room')
    template_name = "rooms/all_rooms.html"
    paginate_by = 6


class DetailRoom(DetailView):
    """ Информация по отдельной комнате """
    model = Room
    context_object_name = "room"
    template_name = "rooms/detail_room.html"

    def get_object(self, queryset=None):
        return Room.objects.select_related('type', 'photos_of_room').get(number=self.kwargs.get("number"))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['regulations_list'] = Regulations.objects.filter(type_room=self.get_object().type)
        context['review_list'] = Review.objects.filter(room=self.get_object()).order_by('-pub_date').select_related(
            'author')
        context['num_of_review'] = len(context['review_list'])
        return context


class AllReserves(LoginRequiredMixin, ListView):
    """ Вывод всех броней пользователя"""
    context_object_name = 'reserve_list'
    template_name = "rooms/all_reserves.html"

    def get_queryset(self):
        return Reserve.objects.filter(client=self.request.user).order_by('-id').select_related('review')


class AddReview(LoginRequiredMixin, CreateView):
    """ Добавление отзыва """
    template_name = 'rooms/add_review.html'
    form_class = ReviewForm
    success_url = reverse_lazy('all_reserves')

    def post(self, request, *args, **kwargs):
        room = self.get_object().room
        room.save()
        return super().post(request, *args, **kwargs)

    def get_object(self, queryset=None):
        reserve = Reserve.objects.select_related('client', 'room').get(pk=self.kwargs.get("pk"))
        if not reserve.client == self.request.user:
            raise Http404
        return reserve

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.reserve = self.get_object()
        form.instance.room = self.get_object().room
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['day_in'] = self.get_object().day_in
        context['day_out'] = self.get_object().day_out
        context['room_reserve'] = self.get_object().room
        return context


class ReserveRoom(LoginRequiredMixin, DetailView):
    """ Бронирование комнаты  """
    model = Room
    context_object_name = "room"
    template_name = "rooms/reserve_room.html"

    def get_object(self, queryset=None):
        return Room.objects.select_related('type', 'photos_of_room').get(number=self.kwargs.get("number"))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['regulations_list'] = Regulations.objects.filter(type_room=self.get_object().type)
        context['review_list'] = Review.objects.filter(room=self.get_object()).order_by('-pub_date').select_related(
            'author')

        context['num_of_review'] = len(context['review_list'])
        context['day_in'] = self.request.GET['day_in']
        context['day_out'] = self.request.GET['day_out']
        context['number_of_guests'] = self.request.GET['number_of_guests']
        context['days'] = get_number_of_days(convert_str_to_date(self.request.GET['day_in']),
                                             convert_str_to_date(self.request.GET['day_out']))
        context['full_price'] = self.get_object().price * context['days']
        return context


class Cancel(LoginRequiredMixin, DeleteView):
    """ Отмена брони """
    model = Reserve()
    template_name = 'rooms/cancel.html'
    success_url = reverse_lazy('all_reserves')

    def get_object(self, queryset=None):
        reserve = Reserve.objects.select_related('client').get(pk=self.kwargs.get("pk"))
        if not reserve.client == self.request.user:
            raise Http404
        return reserve

    def post(self, request, *args, **kwargs):
        if not DT.datetime.now().date() > self.get_object().day_out:
            send_email_cancel(request.user.email)
        return super().post(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if DT.datetime.now().date() < self.get_object().day_in:
            context['days'] = get_number_of_days(self.get_object().day_in, self.get_object().day_out)
            context['delay'] = False
        elif DT.datetime.now().date() == self.get_object().day_in:
            context['days'] = get_number_of_days(self.get_object().day_in, self.get_object().day_out) - 1
            context['delay'] = False
        else:
            if DT.datetime.now().date() > self.get_object().day_out:
                context['days'] = 0
                context['delay'] = True
            else:
                context['days'] = get_number_of_days(DT.datetime.now().date(), self.get_object().day_out)
                context['delay'] = False
        cost = self.get_object().room.price * context['days']
        context[
            'message'] = f"Вам вернется стоимость за {context['days']} дней с {self.get_object().day_in} по {self.get_object().day_out} в размере {cost} рублей. "
        return context


class ListFreeRooms(ListView, LoginRequiredMixin):
    """ Список свободных номеров """
    context_object_name = 'rooms'
    template_name = "rooms/list_free_rooms.html"
    paginate_by = 6

    def get_queryset(self):
        free_rooms_list = Room.objects.select_related('type').filter(
            number_of_guests__gte=int(self.request.GET['number_of_guests']))
        free_rooms_number_list = []
        for room in free_rooms_list:
            if check_availability(room,
                                  convert_str_to_date(self.request.GET['day_in']),
                                  convert_str_to_date(self.request.GET['day_out'])):
                free_rooms_number_list.append(room.number)
        if check_dates_of_user(self.request.user,
                               convert_str_to_date(self.request.GET['day_in']),
                               convert_str_to_date(self.request.GET['day_out'])):
            return Room.objects.select_related('type').filter(number__in=free_rooms_number_list).order_by('number')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['day_in'] = self.request.GET['day_in']
        context['day_out'] = self.request.GET['day_out']
        context['number_of_guests'] = self.request.GET['number_of_guests']
        return context


class Pay(LoginRequiredMixin, View):
    """ Оплата брони (заглушка)"""

    def get(self, request, *args, **kwargs):
        if check_dates_of_user(request.user,
                               convert_str_to_date(request.GET['day_in']),
                               convert_str_to_date(request.GET['day_out'])):
            reserve = Reserve(day_in=request.GET['day_in'],
                              day_out=request.GET['day_out'],
                              room=get_object_or_404(Room, number=self.kwargs.get("number")),
                              number_of_guests=request.GET['number_of_guests'],
                              client=request.user)
            reserve.save()
            message = 'Номер успешно забронирован. Детали бронирования были отправлены вам на электронную почту. Так ' \
                      'же информацию о брони вы можете посмотреть в разделе "Мои резервы". '
            send_email(request.user.first_name, reserve.room, reserve.day_in, reserve.day_out, reserve.number_of_guests,
                       request.user.email)
        else:
            message = 'Ошибка оплаты.'
        return render(request, 'rooms/pay.html', {'message': message, })
