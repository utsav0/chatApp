# Generated by Django 4.0.5 on 2022-07-26 06:39

import datetime
from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('talk', '0011_alter_message_date_and_time_alter_newuser_unique_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='date_and_time',
            field=models.DateTimeField(default=datetime.datetime(2022, 7, 26, 12, 9, 56, 977794)),
        ),
        migrations.AlterField(
            model_name='newuser',
            name='unique_id',
            field=models.CharField(default=uuid.uuid4, max_length=21),
        ),
    ]