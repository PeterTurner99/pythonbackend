from django.contrib import admin
from .models import CalendarAppointment
# Register your models here.


@admin.register(CalendarAppointment)
class CalendarAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'duration']
    readonly_fields = ['duration']

    fieldsets = [
        (None,
        {
            "fields": ["user", ("start", "end","duration"), "title", "description"],

        })
    ]
