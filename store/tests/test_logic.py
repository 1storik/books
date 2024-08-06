from django.contrib.auth.models import User
from django.test import TestCase

from store.logic import set_rating
from store.models import Book, UserBookRelation


class SetRatingTestCases(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', first_name='test', last_name='test')
        self.user2 = User.objects.create_user(username='testuser2', first_name='test2', last_name='test2')
        self.user3 = User.objects.create_user(username='testuser3', first_name='test3', last_name='test3')
        self.book_1 = Book.objects.create(name='Test Book 1', price=25, author='Author 1', owner=self.user)
        self.book_2 = Book.objects.create(name='Test Book 2', price=55, author='Author 1')
        UserBookRelation.objects.create(book=self.book_1, user=self.user, like=True, rate=5)
        UserBookRelation.objects.create(book=self.book_1, user=self.user2, like=True, rate=5)
        UserBookRelation.objects.create(book=self.book_1, user=self.user3, like=True, rate=4)

        UserBookRelation.objects.create(book=self.book_2, user=self.user, like=True, rate=3)
        UserBookRelation.objects.create(book=self.book_2, user=self.user2, like=True, rate=4)
        UserBookRelation.objects.create(book=self.book_2, user=self.user3, like=False)

    def test_ok(self):
        set_rating(self.book_1)
        self.book_1.refresh_from_db()
        self.assertEqual('4.67',str(self.book_1.rating))
