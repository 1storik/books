from django.db.models import Count, Case, When, Avg, Exists, Sum
from rest_framework.test import APITestCase

from store.models import Book, UserBookRelation
from django.contrib.auth.models import User
from store.serializers import BookSerializer


class BookSerializerTestCase(APITestCase):
    def test_ok(self):
        self.user = User.objects.create_user(username='testuser', first_name='test', last_name='test')
        self.user2 = User.objects.create_user(username='testuser2', first_name='test2', last_name='test2')
        self.user3 = User.objects.create_user(username='testuser3', first_name='test3', last_name='test3')
        book_1 = Book.objects.create(name='Test Book 1', price=25, author='Author 1', owner=self.user)
        book_2 = Book.objects.create(name='Test Book 2', price=55, author='Author 1')
        UserBookRelation.objects.create(book=book_1, user=self.user, like=True, rate=5)
        UserBookRelation.objects.create(book=book_1, user=self.user2, like=True, rate=5)
        user_book_3 = UserBookRelation.objects.create(book=book_1, user=self.user3, like=True, rate=4)
        user_book_3.rate = 4
        user_book_3.save()

        UserBookRelation.objects.create(book=book_2, user=self.user, like=True, rate=3)
        UserBookRelation.objects.create(book=book_2, user=self.user2, like=True, rate=4)
        UserBookRelation.objects.create(book=book_2, user=self.user3, like=False)
        books = Book.objects.all().annotate(
            annotated_likes=Count(Case(When(userbookrelation__like=True, then=1)))
        ).order_by('id')
        data = BookSerializer(books, many=True).data
        expected_data = [
            {
                'id': book_1.id,
                'name': 'Test Book 1',
                'price': '25.00',
                'author': 'Author 1',
                'annotated_likes': 3,
                'rating': '4.67',
                'owner_name': 'testuser',
                'readers': [
                    {
                        'first_name': 'test',
                        'last_name': 'test',
                    },
                    {
                        'first_name': 'test2',
                        'last_name': 'test2',
                    },
                    {
                        'first_name': 'test3',
                        'last_name': 'test3',
                    }
                ]
            },
            {
                'id': book_2.id,
                'name': 'Test Book 2',
                'price': '55.00',
                'author': 'Author 1',
                'annotated_likes': 2,
                'rating': '3.50',
                'owner_name': '',
                'readers': [
                    {
                        'first_name': 'test',
                        'last_name': 'test',
                    },
                    {
                        'first_name': 'test2',
                        'last_name': 'test2',
                    },
                    {
                        'first_name': 'test3',
                        'last_name': 'test3',
                    }
                ]
            }
        ]

        print(data)

        self.assertEqual(expected_data, data)

    def test_like_count(self):
        self.user = User.objects.create_user(username='testuser', first_name='test', last_name='test')
        self.user2 = User.objects.create_user(username='testuser2', first_name='test2', last_name='test2')
        self.user3 = User.objects.create_user(username='testuser3', first_name='test3', last_name='test3')
        book_1 = Book.objects.create(name='Test Book 1', price=25, author='Author 1', owner=self.user)
        book_2 = Book.objects.create(name='Test Book 2', price=55, author='Author 1')
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
                'annotated_likes': 3,
                'owner_name': 'testuser',
                'rating': None,
                'readers': [
                    {
                        'first_name': 'test',
                        'last_name': 'test',
                    },
                    {
                        'first_name': 'test2',
                        'last_name': 'test2',
                    },
                    {
                        'first_name': 'test3',
                        'last_name': 'test3',
                    }
                ]
            },
            {
                'id': book_2.id,
                'name': 'Test Book 2',
                'price': '55.00',
                'author': 'Author 1',
                'annotated_likes': 2,
                'owner_name': '',
                'rating': None,
                'readers': [
                    {
                        'first_name': 'test',
                        'last_name': 'test',
                    },
                    {
                        'first_name': 'test2',
                        'last_name': 'test2',
                    },
                    {
                        'first_name': 'test3',
                        'last_name': 'test3',
                    }
                ]
            }
        ]
        self.assertEqual(expected_data, data)
