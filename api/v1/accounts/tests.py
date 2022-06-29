from django.test import TestCase
from rest_framework import status
from rest_framework.test import APITestCase

class RegistrationTestCase(APITestCase):

    def registration_view(self):
        data = {
            'email': "tester@gmail.com",
            'phone_number': "99898451682",
            'password': "strong_password",
            'password2': "strong_password",
            'f_name': "toshmatjon",
            "l_name": "eshmatov",
            "sex": "erkak"
        }
        response = self.client.post('/api/v1/account/register', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

