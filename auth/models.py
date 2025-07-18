from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    max_bookings_at_once = models.IntegerField(default=5)
    
    
class Flag(models.Model):
    name = models.CharField(max_length=100)
    active = models.BooleanField(default=True)