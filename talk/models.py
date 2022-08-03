from datetime import datetime
from django.db import models
from datetime import datetime

# Create your models here.

# for user data


class NewUser(models.Model):
    models.SlugField(max_length=255)
    id = models.AutoField(primary_key=True)
    unique_id = models.CharField(max_length=21,)
    firstName = models.CharField(max_length=150, default=None)
    lastName = models.CharField(max_length=150, default=None)
    userEmail = models.CharField(max_length=150, default=None)
    userPassword = models.CharField(max_length=150, default=None)

    def __str__(self):
        return self.firstName

# for message data

class Message(models.Model):
    combo = models.CharField(max_length=20, default="")
    sender = models.CharField(max_length=20)
    date_and_time = models.DateTimeField(default=datetime.now())
    message = models.TextField()

    def __str__(self):
        return self.combo
