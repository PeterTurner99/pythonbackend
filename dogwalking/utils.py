from collections import defaultdict
from datetime import timedelta
from django.db.models import Q
from django.forms import model_to_dict


def date_range(start_date, length):
    for n in range(length):
        yield start_date + timedelta(days=n)


def tasks_from_date_range(
    start_date, length, user, email_filter=False, title_filter=False
):
    from .models import CalendarAppointment

    calendar_appointments = CalendarAppointment.objects.filter(user=user)
    if email_filter:
        calendar_appointments = calendar_appointments.filter(
            Q(booked_email__icontains=email_filter)
            | Q(booked_user__email__icontains=email_filter)
        )
    if title_filter:
        calendar_appointments = calendar_appointments.filter(
            title__icontains=title_filter
        )
    calendar_appointments = calendar_appointments.order_by("start")
    date_dictionary = defaultdict(
        lambda: {
            0: [],
            1: [],
            2: [],
            3: [],
            4: [],
            5: [],
            6: [],
            7: [],
            8: [],
            9: [],
            10: [],
            11: [],
            12: [],
            13: [],
            14: [],
            15: [],
            16: [],
            17: [],
            18: [],
            19: [],
            20: [],
            21: [],
            22: [],
            23: [],
        }
    )
    for date in date_range(start_date, length):
        for dated_calendar_appointment in calendar_appointments.filter(
            start__date=date
        )[:100]:
            hour = dated_calendar_appointment.start.hour
            date_dictionary[date.isoformat()][hour].append(
                model_to_dict(dated_calendar_appointment)
            )
    return date_dictionary
