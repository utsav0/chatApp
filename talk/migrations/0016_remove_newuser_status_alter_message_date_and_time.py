# Generated by Django 4.0.5 on 2022-07-30 03:46

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('talk', '0015_alter_message_date_and_time_alter_newuser_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='newuser',
            name='status',
        ),
        migrations.AlterField(
            model_name='message',
            name='date_and_time',
            field=models.DateTimeField(default=datetime.datetime(2022, 7, 30, 9, 16, 33, 873531)),
        ),
    ]