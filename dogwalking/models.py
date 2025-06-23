from django.db import models
from django.contrib.auth import get_user_model
from django.contrib import admin
User = get_user_model()
# Create your models here.


class CalendarAppointment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    start = models.DateTimeField()
    end = models.DateTimeField()
    title = models.CharField(max_length=100)
    description = models.TextField()
    
    @property
    @admin.display(ordering="start",
        description="Duration",
        boolean=False,)
    def duration(self):
        return ((self.end - self.start).total_seconds() // 60)