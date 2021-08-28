from django.test import TestCase
from product.models import Book, Author, Category
from django.utils import timezone
import tempfile


# from django.core.urlresolvers import reverse


# models test
# class BookTest(TestCase):
#
#     def create_book(self, title="test book", description="test description", inventory=3, price=100000):
#         image = tempfile.NamedTemporaryFile(suffix=".jpg").name
#         author = Author.objects.create(first_name="kosar", last_name='karbasi')
#         category = Category.objects.create(name='test')
#         return Book.objects.create(title=title, description=description, category=category, author=author,
#                                    inventory=inventory, price=price, image=image, created=timezone.now())
#
#     def test_book_creation(self):
#         w = self.create_book()
#         self.assertTrue(isinstance(w, Book))
#         self.assertEqual(w.__unicode__(), w.title)
