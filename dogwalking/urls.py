from django.urls import path
from .views import Book, BookViewRange

urlpatterns = [
    path("book/", Book.as_view(), name="book"),
    path("book/week/", BookViewRange.as_view(), name="bookrange"),
]
