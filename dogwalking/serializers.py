from rest_framework import serializers
from .models import CalendarAppointment

class CalendarAppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = CalendarAppointment
        fields = ['id', "user","start","end","title","description"]