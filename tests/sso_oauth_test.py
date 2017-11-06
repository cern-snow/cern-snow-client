import unittest

from tests.test_base import TestBase

import os


class SsoOAuthTest(unittest.TestCase, TestBase):

    short_description_prefix = "snow client sso oauth unit test"

    @staticmethod
    def make_good_session():
        good_sso_oauth_config_file = 'tests/config_files/sso_oauth_good.yaml'
        oauth_client_secret = TestBase.get_password('oauth_client_secret_good')

        s = TestBase.make_session(good_sso_oauth_config_file)
        s.set_oauth_client_secret(oauth_client_secret)
        return s

    @staticmethod
    def remove_files():
        os.remove('sso_oauth_cookie.txt')
        os.remove('token_file.npy')

    def test_get_incident(self):
        s = SsoOAuthTest.make_good_session()
        TestBase.test_get_incident(self, s)
        SsoOAuthTest.remove_files()

    def test_insert_incident(self):
        s = SsoOAuthTest.make_good_session()
        TestBase.test_insert_incident(self, s)
        SsoOAuthTest.remove_files()

    def test_update_incident(self):
        s = SsoOAuthTest.make_good_session()
        TestBase.test_update_incident(self, s)
        SsoOAuthTest.remove_files()

    def test_session_persistance(self):
        s = SsoOAuthTest.make_good_session()
        TestBase.test_session_persistance(self, s)
        SsoOAuthTest.remove_files()


if __name__ == '__main__':
    unittest.main()  # for compatibility with Python2.6 unittest
