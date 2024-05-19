from django.shortcuts import render
from rest_framework import viewsets

from store.models import Book
from store.serializers import BookSerializer


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

