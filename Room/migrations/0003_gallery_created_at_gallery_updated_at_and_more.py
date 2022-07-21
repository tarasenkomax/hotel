# Generated by Django 4.0.6 on 2022-07-21 08:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Room', '0002_hotel_created_at_hotel_updated_at_room_created_at_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='gallery',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default='2022-07-21 08:36:03.178743 +00:00'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='gallery',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='regulations',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default='2022-07-21 08:36:03.178743 +00:00'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='regulations',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='reserve',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default='2022-07-21 08:36:03.178743 +00:00'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='reserve',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='review',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default='2022-07-21 08:36:03.178743 +00:00'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='review',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='typeroom',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default='2022-07-21 08:36:03.178743 +00:00'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='typeroom',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
