from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


from store.models import Book
from store.serializers import BookSerializer


class BookApiTestCase(APITestCase):
    def setUp(self):
        self.book_1 = Book.objects.create(name='Test Book 1', price=25, author='Author 1')
        self.book_2 = Book.objects.create(name='Test Book 2', price=55, author='Author 5')
        self.book_3 = Book.objects.create(name='Test Book Author 1', price=55, author='Author 2')

    def test_get(self):
        url = reverse('book-list')
        response = self.client.get(url, data={'price': 55})
        serializer_data = BookSerializer([self.book_1, self.book_2, self.book_3], many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    def test_get_filter(self):
        url = reverse('book-list')
        response = self.client.get(url, data={'search': 'Author 1'})
        serializer_data = BookSerializer([self.book_1, self.book_3], many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    def test_get_ordering(self):
        url = reverse('book-list')
        response = self.client.get(url, data={'ordering': 'price'})
        serializer_data = BookSerializer([self.book_1, self.book_2, self.book_3], many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)
