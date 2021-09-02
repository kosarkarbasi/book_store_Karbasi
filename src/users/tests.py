from django.contrib.auth import get_user_model
from django.test import TestCase


# Create your tests here.
class UserTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email='ali@ali.com',
            password='1234@1234',
            type='ADMIN'
        )
