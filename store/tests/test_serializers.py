from django.db.models import Count, Case, When, Avg, Exists, Sum
from rest_framework.test import APITestCase

from store.models import Book, UserBookRelation
from django.contrib.auth.models import User
from store.serializers import BookSerializer


class BookSerializerTestCase(APITestCase):
    def test_ok(self):
        book_1 = Book.objects.create(name='Test Book 1', price=25, author='Author 1')
        book_2 = Book.objects.create(name='Test Book 2', price=55, author='Author 1')
        self.user = User.objects.create_user(username='testuser')
        self.user2 = User.objects.create_user(username='testuser2')
        self.user3 = User.objects.create_user(username='testuser3')
        UserBookRelation.objects.create(book=book_1, user=self.user, like=True, rate=5)
        UserBookRelation.objects.create(book=book_1, user=self.user2, like=True, rate=5)
        UserBookRelation.objects.create(book=book_1, user=self.user3, like=True, rate=4)

        UserBookRelation.objects.create(book=book_2, user=self.user, like=True, rate=3)
        UserBookRelation.objects.create(book=book_2, user=self.user2, like=True, rate=4)
        UserBookRelation.objects.create(book=book_2, user=self.user3, like=False)
        books = Book.objects.all().annotate(
            annotated_likes=Count(Case(When(userbookrelation__like=True, then=1))),
            rating=Avg('userbookrelation__rate')
        ).order_by('id')
        data = BookSerializer(books, many=True).data
        expected_data = [
            {
                'id': book_1.id,
                'name': 'Test Book 1',
                'price': '25.00',
                'author': 'Author 1',
                'likes_count': 3,
                'annotated_likes': 3,
                'rating': '4.67',
            },
            {
                'id': book_2.id,
                'name': 'Test Book 2',
                'price': '55.00',
                'author': 'Author 1',
                'likes_count': 2,
                'annotated_likes': 2,
                'rating': '3.50',
            }
        ]

        self.assertEqual(expected_data, data)

    def test_like_count(self):
        book_1 = Book.objects.create(name='Test Book 1', price=25, author='Author 1')
        book_2 = Book.objects.create(name='Test Book 2', price=55, author='Author 1')
        self.user = User.objects.create_user(username='testuser')
        self.user2 = User.objects.create_user(username='testuser2')
        self.user3 = User.objects.create_user(username='testuser3')
        UserBookRelation.objects.create(book=book_1, user=self.user, like=True)
        UserBookRelation.objects.create(book=book_1, user=self.user2, like=True)
        UserBookRelation.objects.create(book=book_1, user=self.user3, like=True)

        UserBookRelation.objects.create(book=book_2, user=self.user, like=True)
        UserBookRelation.objects.create(book=book_2, user=self.user2, like=True)
        UserBookRelation.objects.create(book=book_2, user=self.user3, like=False)
        books = Book.objects.all().annotate(
            annotated_likes=Count(Case(When(userbookrelation__like=True, then=1)))).order_by('id')
        data = BookSerializer(books, many=True).data
        expected_data = [
            {
                'id': book_1.id,
                'name': 'Test Book 1',
                'price': '25.00',
                'author': 'Author 1',
                'likes_count': 3,
                'annotated_likes': 3,
            },
            {
                'id': book_2.id,
                'name': 'Test Book 2',
                'price': '55.00',
                'author': 'Author 1',
                'likes_count': 2,
                'annotated_likes': 2,
            }
        ]
        self.assertEqual(expected_data, data)
