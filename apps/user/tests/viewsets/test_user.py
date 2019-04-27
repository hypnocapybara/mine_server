from django.contrib.auth import get_user_model

from apps.main.tests.api_test_case import APITestCase



class UserViewSetTestCase(APITestCase):
    def test_current_unauthorized(self):
        resp = self.client.get('/user/current/')
        self.assertForbidden(resp)

    def test_current_authorized(self):
        self.authenticate(self.first_user)
        resp = self.client.get('/user/current/')
        self.assertSuccessResponse(resp)
        self.assertEqual(resp.data['username'], self.first_user.username)
        self.assertIsNone(resp.data['current_game'])

    def test_create_already_exists(self):
        resp = self.client.post('/user/', {
            'username': self.first_user.username,
            'password': '1234'
        })
        self.assertBadRequest(resp)

    def test_create_success(self):
        resp = self.client.post('/user/', {
            'username': 'newuser',
            'password': '1234'
        })
        self.assertSuccessResponse(resp)

        data = resp.data
        user_pk = data['pk']
        user_from_db = get_user_model().objects.get(pk=user_pk)
        self.assertEqual(user_from_db.username, data['username'])
