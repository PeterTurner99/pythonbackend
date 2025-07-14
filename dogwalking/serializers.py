from rest_framework import serializers
from .models import CalendarAppointment
from django.db.models import Q


class CalendarAppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = CalendarAppointment
        fields = [
            "id",
            "user",
            "start",
            "end",
            "title",
            "description",
            "booked_user",
            "booked_email",
            "booked_name",
        ]

    def validate(self, data):
        if data.get("end") < data.get("start"):
            raise serializers.ValidationError("Start date must be before end date")
        booked_user = data.get("booked_user", False)
        if booked_user:
            max_bookings_at_once = booked_user.max_bookings_at_once
            current_bookings = CalendarAppointment.objects.filter(
                booked_user=booked_user
            )
            start = data.get('start')
            end = data.get('end')
            filtered_current_bookings = current_bookings.filter(
                Q(start__gt=start, start__lt=end) | Q(end__gt=start, start__lt=start)
            )
            booking_count = filtered_current_bookings.count()
            if booking_count >= max_bookings_at_once + 1:
                raise serializers.ValidationError("That person is not available")
            # overlap
            #   start_1 < start_2 and end_1 > start_2
            #   start_1 < end_2 and  start_1 > start_2
            #
            #
        return super().validate(data)
