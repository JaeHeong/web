# Generated by Django 4.0.7 on 2022-09-23 13:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blogapp', '0004_board_current_time'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='board',
            name='current_time',
        ),
    ]