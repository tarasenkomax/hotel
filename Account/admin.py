from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    """ Пользователи """
    add_form = CustomUserCreationForm
    model = CustomUser
    list_display = ('email', 'first_name', 'last_name', 'is_superuser', 'is_staff', 'is_active')
    list_filter = ('is_superuser', 'is_staff', 'is_active')
    readonly_fields = ('last_login', 'date_joined', 'created_at', 'updated_at')
    fieldsets = (
        (None, {'fields': (
            'email', 'last_name', 'first_name', 'phone', 'date_of_birth', 'photo', 'last_login', 'date_joined')}),
        ('Разрешения', {'fields': ('is_superuser', 'is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {'classes': ('wide',),
                'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active')}),
    )
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)


admin.site.register(CustomUser, CustomUserAdmin)

admin.site.site_title = 'Панель Админимтратора Отеля'
admin.site.site_header = 'Панель Администратора Отеля'
