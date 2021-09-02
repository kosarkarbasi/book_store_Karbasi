from django.test import TestCase


# Create your tests here.
class PagesTest(TestCase):
    def test_home_page(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 302)

    def test_about_page(self):
        response = self.client.get('/about/')
        self.assertEqual(response.status_code, 200)
