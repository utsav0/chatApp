# Generated by Django 4.0.5 on 2022-07-17 06:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('talk', '0002_rename_newusers_newuser'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='newuser',
            name='email',
        ),
        migrations.RemoveField(
            model_name='newuser',
            name='fNmame',
        ),
        migrations.RemoveField(
            model_name='newuser',
            name='lName',
        ),
        migrations.RemoveField(
            model_name='newuser',
            name='password',
        ),
        migrations.AddField(
            model_name='newuser',
            name='firstName',
            field=models.CharField(default=None, max_length=50),
        ),
        migrations.AddField(
            model_name='newuser',
            name='lastName',
            field=models.CharField(default=None, max_length=50),
        ),
        migrations.AddField(
            model_name='newuser',
            name='userEmail',
            field=models.CharField(default=None, max_length=50),
        ),
        migrations.AddField(
            model_name='newuser',
            name='userPassword',
            field=models.CharField(default=None, max_length=50),
        ),
        migrations.AlterField(
            model_name='newuser',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
