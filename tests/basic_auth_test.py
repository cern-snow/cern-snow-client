import unittest

from tests.test_base import TestBase

import os


class BasicAuthenticationTest(unittest.TestCase, TestBase):

    short_description_prefix = "snow client basic auth unit test"

    @staticmethod
    def make_good_session():
        good_basic_auth_config_file = 'tests/config_files/basic_good.yaml'
        basic_auth_password = TestBase.get_password('basic_good')

        s = TestBase.make_session(good_basic_auth_config_file)
        s.set_basic_auth_password(basic_auth_password)
        return s

    @staticmethod
    def remove_cookie():
        os.remove('basic_cookie.txt')

    def test_get_incident(self):
        s = BasicAuthenticationTest.make_good_session()
        TestBase.base_test_get_incident(self, s)
        BasicAuthenticationTest.remove_cookie()

    def test_insert_incident(self):
        s = BasicAuthenticationTest.make_good_session()
        TestBase.base_test_insert_incident(self, s)
        BasicAuthenticationTest.remove_cookie()

    def test_update_incident(self):
        s = BasicAuthenticationTest.make_good_session()
        TestBase.base_test_update_incident(self, s)
        BasicAuthenticationTest.remove_cookie()

    def test_session_persistance(self):
        s = BasicAuthenticationTest.make_good_session()
        TestBase.base_test_session_persistance(self, s)
        BasicAuthenticationTest.remove_cookie()


if __name__ == '__main__':
    unittest.main()  # for compatibility with Python2.6 unittest
