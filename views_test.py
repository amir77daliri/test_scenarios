from django.test import TestCase
from .models import Author, Book
import datetime

class View_Test(TestCase):

    def setUp(self):
        p1 = Author.objects.create(first_name="amir", last_name="daliri", date_of_birth="1998-8-15")
        p2 = Author.objects.create(first_name="ali", last_name="amiri", date_of_birth="2000-6-20",date_of_death="2021-3-10")
        p3 = Author.objects.create(first_name="ali", last_name="amiri", date_of_birth="1950-6-20",date_of_death="2021-3-10")
        book_1 = Book.objects.create(title="harry", author=p1, summary="this is harry book", date_of_publish="2000-2-2")
        book_2 = Book.objects.create(title="potter", author=p2, summary="this is potter book", date_of_publish="1998-2-2")
        book_3 = Book.objects.create(title="j.k.rolling", author=p3, summary="this is j.k.rolling book", date_of_publish="1950-2-2")

    def test_view(self):
        book_1 = Book.objects.get(title="harry")
        book_2 = Book.objects.get(title="potter")
        book_3 = Book.objects.get(title="j.k.rolling")
        response = self.client.get('/booklist/25/25/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'booklist.html')
        good_books = [book_1, book_2]
        bad_books = [book_3]
        self.assertEqual(response.context.get('good_books'), good_books)
        self.assertEqual(response.context.get('bad_books'), bad_books)