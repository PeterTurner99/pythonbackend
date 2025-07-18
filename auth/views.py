import os
from django.conf import settings
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny

from auth.models import Flag
from auth.utils import check_flag
from .forms import RegistrationForm
from rest_framework.serializers import DateTimeField
from django.contrib.auth.signals import user_logged_in
from django.utils import timezone
from knox.models import get_token_model
from knox.settings import knox_settings
from .serializers import UserSerializer
from google.oauth2 import id_token
from google.auth.transport import requests
from django.contrib.auth import get_user_model

User = get_user_model()


class Check(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        return Response({})


class ViewProfile(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        return_dict = {
            "email": user.email,
            "username": user.username,
            "max_bookings_at_once": user.max_bookings_at_once,
        }
        return Response(return_dict)

    def post(self, request):
        data = request.data
        user = request.user
        userSerializer = UserSerializer(user, data)
        if userSerializer.is_valid():
            userSerializer.save()
            return Response(
                {
                    "email": userSerializer.instance.email,
                    "username": userSerializer.instance.username,
                    "max_bookings_at_once": userSerializer.instance.max_bookings_at_once,
                }
            )
        return Response(userSerializer.errors, status=400)


class Register(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request):
        data = request.data
        # username = data.get('username')
        # password = data.get('password')
        # email = data.get('email')
        registration_form = RegistrationForm(data)
        if not registration_form.is_valid():
            return Response(registration_form.errors, status=400)

        user_obj = registration_form.save()
        token_limit_per_user = self.get_token_limit_per_user()
        self.user = user_obj
        if token_limit_per_user is not None:
            now = timezone.now()
            token = user_obj.auth_token_set.filter(expiry__gt=now)
            if token.count() >= token_limit_per_user:
                return Response(
                    {"error": "Maximum amount of tokens allowed per user exceeded."},
                    status=status.HTTP_403_FORBIDDEN,
                )
        instance, token = self.create_token()
        user_logged_in.send(sender=user_obj.__class__, request=request, user=user_obj)
        return self.get_post_response(user_obj, token, instance)

    def get_context(self):
        return {"request": self.request, "format": self.format_kwarg, "view": self}

    def get_token_ttl(self):
        return knox_settings.TOKEN_TTL

    def get_token_prefix(self):
        return knox_settings.TOKEN_PREFIX

    def get_token_limit_per_user(self):
        return knox_settings.TOKEN_LIMIT_PER_USER

    def get_user_serializer_class(self):
        return knox_settings.USER_SERIALIZER

    def get_expiry_datetime_format(self):
        return knox_settings.EXPIRY_DATETIME_FORMAT

    def format_expiry_datetime(self, expiry):
        datetime_format = self.get_expiry_datetime_format()
        return DateTimeField(format=datetime_format).to_representation(expiry)

    def create_token(self):
        token_prefix = self.get_token_prefix()
        return get_token_model().objects.create(
            user=self.user, expiry=self.get_token_ttl(), prefix=token_prefix
        )

    def get_post_response_data(self, user, token, instance):
        UserSerializer = self.get_user_serializer_class()

        data = {"expiry": self.format_expiry_datetime(instance.expiry), "token": token}
        if UserSerializer is not None:
            data["user"] = UserSerializer(user, context=self.get_context()).data
        return data

    def get_post_response(self, user, token, instance):
        data = self.get_post_response_data(user, token, instance)
        return Response(data)


class GoogleLogin(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request):
        if not check_flag('google_login'):
            return Response(status=404)
        token = request.data.get("credential")
        try:
            user_data = id_token.verify_oauth2_token(
                token, requests.Request(), settings.GOOGLE_OAUTH_CLIENT_ID
            )
        except ValueError:
            return Response({"error": "Invalid login details."}, status=403)
        email = user_data.get("email")
        first_name = user_data.get("given_name")
        user_filter = User.objects.filter(email=email)
        if user_filter.exists():
            user_obj = user_filter.first()
        else:
            user_obj = User.objects.create_user(
                username=email, first_name=first_name, email=email
            )

        token_limit_per_user = self.get_token_limit_per_user()
        self.user = user_obj
        if token_limit_per_user is not None:
            now = timezone.now()
            token = user_obj.auth_token_set.filter(expiry__gt=now)
            if token.count() >= token_limit_per_user:
                return Response(
                    {"error": "Maximum amount of tokens allowed per user exceeded."},
                    status=status.HTTP_403_FORBIDDEN,
                )
        instance, token = self.create_token()
        user_logged_in.send(sender=user_obj.__class__, request=request, user=user_obj)
        return self.get_post_response(user_obj, token, instance)

    def get_context(self):
        return {"request": self.request, "format": self.format_kwarg, "view": self}

    def get_token_ttl(self):
        return knox_settings.TOKEN_TTL

    def get_token_prefix(self):
        return knox_settings.TOKEN_PREFIX

    def get_token_limit_per_user(self):
        return knox_settings.TOKEN_LIMIT_PER_USER

    def get_user_serializer_class(self):
        return knox_settings.USER_SERIALIZER

    def get_expiry_datetime_format(self):
        return knox_settings.EXPIRY_DATETIME_FORMAT

    def format_expiry_datetime(self, expiry):
        datetime_format = self.get_expiry_datetime_format()
        return DateTimeField(format=datetime_format).to_representation(expiry)

    def create_token(self):
        token_prefix = self.get_token_prefix()
        return get_token_model().objects.create(
            user=self.user, expiry=self.get_token_ttl(), prefix=token_prefix
        )

    def get_post_response_data(self, user, token, instance):
        UserSerializer = self.get_user_serializer_class()

        data = {"expiry": self.format_expiry_datetime(instance.expiry), "token": token}
        if UserSerializer is not None:
            data["user"] = UserSerializer(user, context=self.get_context()).data
        return data

    def get_post_response(self, user, token, instance):
        data = self.get_post_response_data(user, token, instance)
        return Response(data)


class FlagView(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        queryParams = request.query_params.dict()
        flag_name = queryParams.get("flag_name")
        flag_filter = Flag.objects.filter(name=flag_name)
        if flag_filter.exists():
            return Response({"result": flag_filter.first().active})
        return Response({"result": False})
