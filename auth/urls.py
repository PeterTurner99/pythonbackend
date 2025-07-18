from django.urls import path
from .views import Check, Register, ViewProfile, GoogleLogin

urlpatterns = [
    path("Check/", Check.as_view(), name="Check"),
    path("register/", Register.as_view(), name="register"),
    path("profile/", ViewProfile.as_view(), name="profile"),
    path("social/google/", GoogleLogin.as_view(), name="GoogleLogin"),
]
