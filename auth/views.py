from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from .forms import RegistrationForm
from rest_framework.serializers import DateTimeField
from django.contrib.auth.signals import user_logged_in
from django.utils import timezone
from knox.models import get_token_model
from knox.settings import knox_settings


class Check(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        return Response({})

class ViewProfile(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        user = request.user
        return_dict = {
            'email': user.email ,
            'username': user.username ,
            'max_bookings_at_once': user.max_bookings_at_once ,
        }
        return Response(return_dict)
    


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
        user_logged_in.send(
            sender=user_obj.__class__, request=request, user=user_obj
        )
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
