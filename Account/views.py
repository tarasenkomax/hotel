from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic
import datetime as DT
from Account.forms import CustomUserCreationForm, UserSettingsForm
from Account.models import CustomUser


def home(request):
    """Домашняя страница"""
    if request.method == 'POST':
        if request.POST['day_in'] and request.POST['day_out'] and request.POST['number_of_guests']:
            day_in = request.POST['day_in']
            day_out = request.POST['day_out']
            number_of_guests = int(request.POST['number_of_guests'])
            if number_of_guests <= 0:
                return render(request, 'home.html', {'error': 'Введите корректное число гостей'})
            if day_in > day_out:
                return render(request, 'home.html', {'error': 'Выезд не может быть раньше заезда'})
            if day_in == day_out:
                return render(request, 'home.html', {'error': 'Укажите корректные даты'})
            if DT.datetime.strptime(day_in, '%Y-%m-%d').date() <= DT.datetime.now().date():
                return render(request, 'home.html', {'error': 'Нельзя бронировать на прошедшие дни'})
            else:
                return redirect('/list_free_rooms?day_in={0}&day_out={1}&number_of_guests={2}'.format(day_in, day_out,
                                                                                                      number_of_guests))
        else:
            return render(request, 'home.html', {'error': 'Пожалуйста заполните все поля формы'})
    return render(request, 'home.html')


@login_required
def account(request):
    """ Возвращает информацию о пользователе в ЛК"""
    return render(request, 'profile/account.html', {'name': request.user.name,
                                                    'surname': request.user.surname,
                                                    'date_of_birth': request.user.date_of_birth,
                                                    'photo': request.user.photo,
                                                    'phone': request.user.phone,
                                                    'email': request.user.email,
                                                    'patronymic': request.user.patronymic,
                                                    })


@login_required
def account_settings(request):  # TODO не заливаются фотки с ЛК
    """ Заполняет информацию о пользователе в ЛК """
    form = UserSettingsForm()
    if request.method == 'POST':
        # Если профиль заполнен, то вносим изменения
        # Профиль заполнен всегда, так как почта указывается при регистрации
        if CustomUser.objects.exists():
            form = UserSettingsForm(request.POST, request.FILES, instance=request.user)
            if form.is_valid():
                if form.has_changed():
                    form.save()
                    form = UserSettingsForm(instance=request.user)
                    return redirect('account')
                else:
                    return redirect('account')
    else:
        # Если GET
        if CustomUser.objects.exists():
            # Если профиль заполнен, то выводим на экран
            form = UserSettingsForm(instance=request.user)
    return render(request, 'profile/account_settings.html', {'form': form})


class SignUp(generic.CreateView):
    """Регистрация"""
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('home')
    template_name = 'registration/signup.html'

    def form_valid(self, form):
        """Автоматический вход в систему после регистрации"""
        view = super(SignUp, self).form_valid(form)
        email, password = form.cleaned_data.get('email'), form.cleaned_data.get('password1')
        user = authenticate(username=email, password=password)
        login(self.request, user)
        return view
