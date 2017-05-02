from app import app

import unittest


class LoginTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app
        self.app.config['WTF_CSRF_ENABLED'] = False
        self.tester = self.app.test_client(self)
        self.tester.testing = True

    def test_manager_page(self):
        response = self.tester.get('/app/manager')
        self.assertEqual(response.status_code, 404)

    def test_no_id_login(self):
        response = self.tester.post('login', data=dict(first_name='myname', last_name='mylastname'))
        self.assertEqual(response.status_code, 404)
        err = 'טופס לא חוקי'
        assert str.encode(err) in response.data

    def test_invalid_user(self):
        credentials = {'first_name': 'unexisting', 'last_name': 'lastname', 'id_num': 1234}
        response = self.tester.post('login', data=credentials,
                                    follow_redirects=True)
        self.assertEqual(response.status_code, 404)
        err = 'משתמש לא קיים במערכת'
        assert str.encode(err) in response.data


if __name__ == '__main__':
    unittest.main()
