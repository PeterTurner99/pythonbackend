from collections import defaultdict
from datetime import timedelta

from django.forms import model_to_dict


def date_range(start_date, length):
    for n in range(length):
        yield start_date + timedelta(days=n)


def tasks_from_date_range(start_date, length, user):
    from .models import CalendarAppointment

    calendar_appointments = CalendarAppointment.objects.filter(
        user=user).order_by('start')
    date_dictionary = defaultdict(
        lambda:{0:[],1: [],
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
        for dated_calendar_appointment in calendar_appointments.filter(start__date=date):
            hour = dated_calendar_appointment.start.hour
            date_dictionary[date.isoformat()][hour].append(
                model_to_dict(dated_calendar_appointment))
    return date_dictionary
