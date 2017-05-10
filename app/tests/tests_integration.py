# -*- coding: utf-8 -*-

import os
import unittest

from flask_testing import LiveServerTestCase
from selenium import webdriver

from app import app, db
from app.models import User, Party

basedir = os.path.abspath(os.path.dirname(__file__))
class AppTestCase(LiveServerTestCase):
    def create_app(self):
        self.app = app
        self.app.config['TESTING'] = True
        self.app.config['WTF_CSRF_ENABLED'] = False
        self.app.config['LIVESERVER_PORT'] = 8943
        self.app.config['WTF_CSRF_ENABLED'] = False
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'test.db') #'sqlite:///:memory:'
        db.init_app(self.app)
        with self.app.app_context():  # app context
            db.drop_all()
            db.create_all()
            self.populate()

        return self.app

    def populate(self):
        db.session.commit()
        valid_user = User(111111, 'firstName', 'lastName', False)
        valid_party = Party(u'עלה ירוק', 'static/images/yarok.jpeg', 0)
        db.session.add(valid_party)
        db.session.add(valid_user)
        db.session.commit()

    def setUp(self):
        """Setup the test driver and create test users"""
        self.driver = webdriver.PhantomJS()
        self.driver.get(self.get_server_url())

    def tearDown(self):
        self.driver.quit()

    def test_valid_user_selenium(self):
        self.valid_user = User(111111, 'firstName', 'lastName', False)
        self.valid_party = Party(u'עלה ירוק', 'static/images/yarok.jpeg', 0)
        self.first_name = self.driver.find_element_by_id('first_name')
        self.last_name = self.driver.find_element_by_id('last_name')
        self.id_num = self.driver.find_element_by_id('id_num')
        self.login_button = self.driver.find_element_by_id('login_button')
        self.first_name.send_keys(self.valid_user.first_name)
        self.last_name.send_keys(self.valid_user.last_name)
        self.id_num.send_keys(self.valid_user.id)
        self.login_button.submit()
        print(self.driver.title)
        assert 'Home' in self.driver.title

    def test_invalid_user_selenium(self):
        self.first_name = self.driver.find_element_by_id('first_name')
        self.last_name = self.driver.find_element_by_id('last_name')
        self.id_num = self.driver.find_element_by_id('id_num')
        self.login_button = self.driver.find_element_by_id('login_button')
        self.first_name.send_keys('invalidFirstName')
        self.last_name.send_keys('invalidLastName')
        self.id_num.send_keys('invalidID')
        self.login_button.submit()
        print(self.driver.title)
        assert 'Home' not in self.driver.title


if (__name__ == '__main__'):
    unittest.main()