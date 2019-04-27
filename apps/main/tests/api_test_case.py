from rest_framework.test import APITestCase as BaseAPITestCase

from apps.user.factories import UserFactory
from .mixins import APIAssertsMixin


class APITestCase(APIAssertsMixin, BaseAPITestCase):
    def setUp(self):
        super(APITestCase, self).setUp()

        self.first_user = UserFactory(password='password')
        self.second_user = UserFactory(password='password')

    def authenticate(self, user, password='password'):
        auth_resp = self.client.post('/user/login/', {
            'username': user.username,
            'password': password,
        }, format='json')
        self.assertSuccessResponse(auth_resp)

        token = auth_resp.data['token']

        self.client.credentials(
            HTTP_AUTHORIZATION='Token {0}'.format(token)
        )

        return token
