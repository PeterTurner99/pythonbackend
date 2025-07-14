from django.urls import path
from .views import Check, Register

urlpatterns = [
    path("Check/", Check.as_view(), name="Check"),
    path("register/", Register.as_view(), name="register"),
]
