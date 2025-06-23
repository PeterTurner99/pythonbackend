from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from dogwalking.utils import date_range, tasks_from_date_range
from .serializers import CalendarAppointmentSerializer
from .models import CalendarAppointment
from datetime import timedelta, datetime
# Create your views here.


class Book(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data
        start_date = datetime.fromisoformat(data.get('startDate'))
        end_date = datetime.fromisoformat(data.get('endDate'))
        if end_date < start_date:
            return Response({}, status=400)
        processed_data = {
            'user': request.user.pk,
            'start': start_date,
            'end': end_date,
            'title': data.get('title'),
            'description': data.get('description'),
        }
        seralizer = CalendarAppointmentSerializer(data=processed_data)
        if seralizer.is_valid():
            seralizer.save()
            return Response({})
        return Response({}, status=400)

    def get(self, request):
        bookings = CalendarAppointment.objects.filter(
            user=request.user).order_by('start')
        serialized_bookings = CalendarAppointmentSerializer(
            bookings, many=True)
        return JsonResponse(serialized_bookings.data, safe=False)


class BookViewRange(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        queryParams = request.query_params.dict()
        start_date = queryParams.get('date')
        if not start_date:
            start_date = timezone.now()
        else:
            start_date = datetime.fromisoformat(start_date)
        bookings = tasks_from_date_range(start_date, 8, request.user)

        for start_date in date_range(start_date, 7):
            if start_date.isoformat() not in bookings.keys():
                bookings[start_date.isoformat()] = {0:[],1: [],
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
        new_booking_dict = {}
        
        for date_task_date, date_task_list in sorted(bookings.items()):
            new_booking_dict[date_task_date] = date_task_list
            #.append(
            #    { date_task_date: date_task_list})

        return JsonResponse(new_booking_dict, safe=False)
