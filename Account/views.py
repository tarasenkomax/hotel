from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import generic
import datetime as DT

from django.views.generic import DetailView

from Account.forms import CustomUserCreationForm, UserSettingsForm
from Account.models import CustomUser


class Account(LoginRequiredMixin, DetailView):
    """ Возвращает информацию о пользователе в ЛК"""
    model = CustomUser
    template_name = "profile/account.html"
    context_object_name = "user"

    def get_object(self, queryset=None):
        return get_object_or_404(CustomUser, email=self.request.user.email)


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


def home(request):
    """Домашняя страница"""
    if request.method == 'POST':
        if request.POST['day_in'] and request.POST['day_out'] and request.POST['number_of_guests']:
            day_in = DT.datetime.strptime(request.POST['day_in'], '%d.%m.%Y').date()
            day_out = DT.datetime.strptime(request.POST['day_out'], '%d.%m.%Y').date()
            number_of_guests = int(request.POST['number_of_guests'][0])
            return redirect('/list_free_rooms?day_in={0}&day_out={1}&number_of_guests={2}'.format(day_in, day_out,
                                                                                                  number_of_guests))
        else:
            return render(request, 'home.html', {'error': 'Пожалуйста заполните все поля формы'})
    return render(request, 'home.html')


@login_required
def account_settings(request):
    """ Заполняет информацию о пользователе в ЛК """
    form = UserSettingsForm()
    if request.method == 'POST':
        if CustomUser.objects.exists():
            form = UserSettingsForm(request.POST, request.FILES, instance=request.user)
            if form.is_valid():
                if form.has_changed():
                    form.save()
                    return redirect('account')
                else:
                    return redirect('account')
    else:
        # Если GET
        form = UserSettingsForm(instance=request.user)
    return render(request, 'profile/account_settings.html', {'form': form, 'photo': request.user.photo})
