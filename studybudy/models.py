from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import date

class person(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    gender = models.CharField(max_length=10, null=True, blank=True)
    phone_number = models.CharField(max_length=10, null=True, blank=True)
    date_of_birth = models.DateField(default=date(1999,10,19), null=True, blank=True)


    def __str__(self):
        return self.username