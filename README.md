### Описание:
Веб-приложение должно выполнять следующие задачи:
- регистрация / авторизация пользователей;
- смена / восстановление пароля от учетной записи пользователя;
- просмотр списка всех комнат в отеле (с пагинацией);
- получение списка всех комнат удовлетворяющих введенным пользователем данным (дата заезда, дата выезда, количество гостей) с пагинацией;
- возможность просмотра информации по отдельной комнате (фотографии, стоимость за сутки, описание, отзывы других пользователей, правила комнаты);
- бронирование комнаты;
- возможность оставить отзыв к забронированным комнатам;
- отправка сообщения на почту пользователя, в случае  успешного бронирования;
- отмена бронирования (с уведомлением на почту);
- отображение  всех броней пользователя;
- удаление броней закончившихся больше полугода назад;
- рассылка рекламных писем всем зарегистрированным пользователям раз в 3 месяца;
- панель администратора, позволяющая создавать, просматривать, редактировать и удалять записи в базах данных.

### Необходимое окружение
* Python 3.7+
* PostgreSQL

### Развертывание
1. Скачать с репозитория
2. Установить виратульное окружение Python  
   `python3.7 -m venv venv`
3. Создать файл с переменными окружения согласно шаблону .env.sample в корне проекта
4. Активировать виртуальное окружение  
   `source venv/Scripts/activate`
5. Установить зависимости  
   `pip install -r requirements.txt`
6. Создать миграции  
   `python manage.py makemigrations`
7. Выполнить миграции  
   `python manage.py migrate`
8. Создать суперпользователя для доступа к панели администратора  
   `python manage.py createsuperuser`
9. Запустить приложение  
   `python manage.py runserver`
10. Запустить celery beat для периодических задач (рассылка писем и удаление старых броней)  
   `celery -A settings beat`
11. Запустить flower для отслеживания celery (необязательно)  
   `flower -A settings --port=5555`
12. Запустить celery для выполнения celery beat  
   `celery -A settings worker --loglevel=INFO --concurrency 1 -P solo`
