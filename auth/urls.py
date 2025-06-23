from django.urls import path
from .views import check
urlpatterns = [
    path('check/', check.as_view(), name='check')
]
