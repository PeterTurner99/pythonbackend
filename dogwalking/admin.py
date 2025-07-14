from django.contrib import admin
from .models import CalendarAppointment
from django.contrib.auth import get_user_model

User = get_user_model()


@admin.action(description="Set user for testing")
def set_user(modeladmin, request, queryset):
    MAIN_USER_PK = 1
    queryset.update(booked_user=User.objects.get(pk=MAIN_USER_PK))


@admin.register(CalendarAppointment)
class CalendarAdmin(admin.ModelAdmin):
    list_display = ["__str__", "duration"]
    readonly_fields = ["duration"]
    actions = [set_user]
    fieldsets = [
        (
            None,
            {
                "fields": [
                    ("user", "booked_user"),
                    ("start", "end", "duration"),
                    "title",
                    "description",
                ],
            },
        )
    ]
