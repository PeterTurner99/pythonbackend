from datetime import datetime

# Create your views here.
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.utils import timezone
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from dogwalking.utils import date_range, tasks_from_date_range

from .models import CalendarAppointment
from .serializers import CalendarAppointmentSerializer

User = get_user_model()
NUMBER_OF_DAYS_IN_WEEK = 7


class Book(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data
        data = data.get("data")
        start_date = datetime.fromisoformat(data.get("startDate"))
        end_date = datetime.fromisoformat(data.get("endDate"))
        book_email = data.get("booked_email")
        book_user = User.objects.filter(email=book_email) 
        processed_data = {
            "user": request.user.pk,
            "start": start_date,
            "end": end_date,
            "title": data.get("title"),
            "description": data.get("description"),
        }
        if not book_user.exists():
            book_name = data.get("booked_name")
            processed_data["booked_email"] = book_email
            processed_data["booked_name"] = book_name
        else:
            processed_data["booked_user"] = book_user.first().pk
        seralizer = CalendarAppointmentSerializer(data=processed_data)
        if seralizer.is_valid():
            seralizer.save()
            return Response({})
        
        return Response(seralizer.errors, status=400)

    def get(self, request):
        bookings = CalendarAppointment.objects.filter(user=request.user).order_by(
            "start"
        )
        serialized_bookings = CalendarAppointmentSerializer(bookings, many=True)
        return JsonResponse(serialized_bookings.data, safe=False)


class BookViewRange(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        queryParams = request.query_params.dict()
        start_date = queryParams.get("date")
        if not start_date:
            start_date = timezone.now()
        else:
            start_date = datetime.fromisoformat(start_date)
        bookings = tasks_from_date_range(
            start_date, NUMBER_OF_DAYS_IN_WEEK, request.user
        )

        for start_date in date_range(start_date, NUMBER_OF_DAYS_IN_WEEK):
            if start_date.isoformat() not in bookings.keys():
                bookings[start_date.isoformat()] = {
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
        new_booking_dict = {}

        for date_task_date, date_task_list in sorted(bookings.items()):
            new_booking_dict[date_task_date] = date_task_list

        return JsonResponse(new_booking_dict, safe=False)

    def post(self, request):
        data = request.data
        query_params = request.query_params.dict()
        email_filter = data.get("emailFilter", False)
        title_filter = data.get("titleFilter", False)
        start_date = query_params.get("date")
        if not start_date:
            start_date = timezone.now()
        else:
            start_date = datetime.fromisoformat(start_date)
        bookings = tasks_from_date_range(
            start_date, NUMBER_OF_DAYS_IN_WEEK, request.user, email_filter, title_filter
        )

        for start_date in date_range(start_date, NUMBER_OF_DAYS_IN_WEEK):
            if start_date.isoformat() not in bookings.keys():
                bookings[start_date.isoformat()] = {
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
        new_booking_dict = {}

        for date_task_date, date_task_list in sorted(bookings.items()):
            new_booking_dict[date_task_date] = date_task_list

        return JsonResponse(new_booking_dict, safe=False)
