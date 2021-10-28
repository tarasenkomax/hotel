from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from django.contrib.auth import views as auth_views

from Account import views
from Account.forms import AuthenticationUserForm

urlpatterns = [
    path('', views.home, name='home'),

    # ----- AUTH -----

    path('signup', views.SignUp.as_view(), name='signup'),
    path('login', auth_views.LoginView.as_view(authentication_form=AuthenticationUserForm), name='login'),
    path('logout', auth_views.LogoutView.as_view(next_page='home'), name='logout'),

    # ----- СБРОС ПАРОЛЯ -----
    path('password-reset/',
         auth_views.PasswordResetView.as_view(template_name='password_reset/form.html',
                                              html_email_template_name='password_reset/email.html',
                                              subject_template_name='password_reset/subject_email.txt'),
         name='password_reset'),
    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(template_name='password_reset/done.html'),
         name='password_reset_done'),
    path('password-reset/confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='password_reset/confirm.html'),
         name='password_reset_confirm'),
    path('password-reset/complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name='password_reset/complete.html'),
         name='password_reset_complete'),

    # -----СМЕНА ПАРОЛЯ-----

    path('account/password-change/',
         auth_views.PasswordChangeView.as_view(template_name='password_change/password_change.html'),
         name='password_change'),

    path('account/password-change-done/',
         auth_views.PasswordChangeDoneView.as_view(template_name='password_change/password_change_done.html'),
         name='password_change_done'),


    # -----ЛИЧНЫЙ КАБИНЕТ-----

    path('account/', views.Account.as_view(), name='account'),
    path('account_settings/', views.account_settings, name='account_settings'),

]

