from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    max_bookings_at_once = models.IntegerField(default=5)