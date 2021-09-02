from django.test import TestCase


class BookUrlTest(TestCase):
    def test_book_list_url(self):
        response = self.client.get('/books/')
        self.assertEqual(response.status_code, 200)

    # def test_book_detail_url(self):
    #     response = self.client.get('/book/detail/1')
    #     self.assertEqual(response.status_code, 200)
