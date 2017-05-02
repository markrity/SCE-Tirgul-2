from app import app

import unittest


class LoginTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app
        self.app.config['WTF_CSRF_ENABLED'] = False
        self.tester = self.app.test_client(self)
        self.tester.testing = True

    def test_manager(self):
        response = self.tester.get('/app/manager')
        self.assertEqual(response.status_code, 404)

    def test_login(self):

        response = self.tester.post('login', data=dict(first_name='invalid', last_name='invalid'))
        self.assertEqual(response.status_code, 404)
        err = 'טופס לא חוקי'
        assert str.encode(err) in response.data


if __name__ == '__main__':
    unittest.main()
