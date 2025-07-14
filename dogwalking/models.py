from django.db import models
from django.contrib.auth import get_user_model
from django.contrib import admin

User = get_user_model()
# Create your models here.


class CalendarAppointment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bookee")
    start = models.DateTimeField()
    end = models.DateTimeField()
    title = models.CharField(max_length=100)
    description = models.TextField()
    booked_user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="booker", null=True, blank=True
    )
    booked_email = models.EmailField(null=True, blank=True)
    booked_name = models.CharField(max_length=100, null=True, blank=True)

    @property
    @admin.display(
        ordering="start",
        description="Duration",
        boolean=False,
    )
    def duration(self):
        """Returns duration of booking i.e. length of time in seconds between starting and ending dates
        

        Returns:
            int: Duration in seconds
        """
        return (self.end - self.start).total_seconds() // 60
