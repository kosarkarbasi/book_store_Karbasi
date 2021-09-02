import tempfile
from django.test import TestCase
from product.models import Book


class BookTest(TestCase):
    def setUp(self):
        self.book = Book.objects.create(
            title='test',
            image=tempfile.NamedTemporaryFile(suffix=".jpg").name,
            inventory=12,
            price=120000,
        )
        self.category = self.book.category.create(name='t')
        self.author = self.book.author.create(first_name='kosar', last_name='karbasi')

    def test_create_book(self):
        self.assertEqual(f'{self.book.title}', 'test')
        self.assertEqual(self.book.inventory, 12)
        self.assertEqual(self.book.price, 120000)
        self.assertEqual(self.book.category.all()[0], self.category)
        self.assertEqual(self.book.author.all()[0], self.author)

    def test_book_view_list(self):
        response = self.client.get('/books/')
        self.assertContains(response, 'test')
        self.assertTemplateUsed(response, 'book_list.html')

    def test_book_view_detail(self):
        response = self.client.get('/books/detail/1')
        self.assertContains(response, 'test')
        self.assertTemplateUsed(response, 'book_detail.html')
