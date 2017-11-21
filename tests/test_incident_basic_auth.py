# coding: utf-8

import unittest
import os

from tests.test_base import TestBase
from tests.test_incident_base import TestIncidentBase


class TestIncidentBasicAuthentication(unittest.TestCase, TestIncidentBase):

    short_description_prefix = "snow client - incident unit test - basic auth"

    current_user = TestBase.basic_auth_user

    @classmethod
    def make_good_session(cls):
        good_basic_auth_config_file = 'tests/config_files/basic_good.yaml'
        basic_auth_password = cls.get_password('basic_good')

        s = cls.make_session(good_basic_auth_config_file)
        s.set_basic_auth_password(basic_auth_password)
        return s

    @classmethod
    def remove_cookie(cls):
        try:
            os.remove('basic_cookie.txt')
        except OSError:
            pass

    def test_incident_get(self):
        s = self.make_good_session()
        TestIncidentBase.base_test_incident_get(self, s)
        self.remove_cookie()

    def test_incident_insert(self):
        s = self.make_good_session()
        TestIncidentBase.base_test_incident_insert(self, s)
        self.remove_cookie()

    def test_incident_update(self):
        s = self.make_good_session()
        TestIncidentBase.base_test_incident_update(self, s)
        self.remove_cookie()

    def test_incident_add_comment(self):
        s = self.make_good_session()
        TestIncidentBase.base_test_incident_add_comment(self, s)
        self.remove_cookie()

    def test_incident_add_work_note(self):
        s = self.make_good_session()
        TestIncidentBase.base_test_incident_add_work_note(self, s)
        self.remove_cookie()

    def test_incident_take_in_progress(self):
        s = self.make_good_session()
        TestIncidentBase.base_test_incident_take_in_progress(self, s)
        self.remove_cookie()

    def test_incident_resolve(self):
        s = self.make_good_session()
        TestIncidentBase.base_test_incident_resolve(self, s)
        self.remove_cookie()

    def test_incident_query(self):
        s = self.make_good_session()
        TestIncidentBase.base_test_incident_query(self, s)
        self.remove_cookie()


if __name__ == '__main__':
    unittest.main()  # for compatibility with Python2.6 unittest
