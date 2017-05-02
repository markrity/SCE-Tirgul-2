# -*- coding: utf-8 -*-
import os
import unittest

from app import app, db
from app.models import User, Party
from flask_config import basedir

basedir = os.path.abspath(os.path.dirname(__file__))

class LoginTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app
        self.app.config['WTF_CSRF_ENABLED'] = False
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'test.db')
        self.tester = self.app.test_client(self)
        self.tester.testing = True
        db.init_app(self.app)
        with self.app.app_context():
            db.drop_all()
            db.create_all()
            self.populate_db()

    def test_manager_page(self):
        response = self.tester.get('/app/manager')
        self.assertEqual(response.status_code, 404)

    def test_no_id_login(self):
        response = self.tester.post('login', data=dict(first_name='myname', last_name='mylastname'))
        self.assertEqual(response.status_code, 404)
        err = 'טופס לא חוקי'
        assert err.decode('utf-8') in response.data.decode('utf-8')

    def test_invalid_user(self):
        credentials = {'first_name': 'unexisting', 'last_name': 'lastname', 'id_num': 1234}
        response = self.tester.post('login', data=credentials,
                                    follow_redirects=True)
        self.assertEqual(response.status_code, 404)
        err = 'משתמש לא קיים במערכת'
        resp = response.data.decode('utf-8')
        assert err.decode('utf-8') in resp

    def test_valid_user(self):
        credentials = {'first_name': 'tomer', 'last_name': 'admon', 'id_num': 123456}
        response = self.tester.post('login', data=credentials,
                                    follow_redirects=False)
        self.assertEqual(response.status_code, 302)
        assert 'index' in response.location

    def test_valid_user_already_voted(self):
        credentials = {'first_name': 'max', 'last_name': 'zh', 'id_num': 1234567}
        response = self.tester.post('login', data=credentials,
                                    follow_redirects=True)
        self.assertEqual(response.status_code, 404)
        err = 'המשתמש כבר הצביע'
        assert err.decode('utf-8') in response.data.decode('utf-8')

    def populate_db(self):
        db.session.commit()

        admon = User(123456, 'tomer', 'admon', False)
        max = User(1234567, 'max', 'zh', True)
        yarok = Party(u'עלה ירוק', 'static/images/yarok.jpeg', 0)
        db.session.add(yarok)
        db.session.add(admon)
        db.session.add(max)
        db.session.commit()

    def tearDown(self):
        db.init_app(self.app)
        with self.app.app_context():
            db.drop_all()

if __name__ == '__main__':
    unittest.main()
