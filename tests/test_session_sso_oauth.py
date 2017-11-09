# coding: utf-8

import unittest
import os

from tests.test_session_base import TestSessionBase


class TestSessionSsoOauth(unittest.TestCase, TestSessionBase):

    short_description_prefix = "snow client - session unit test - sso oauth"

    @classmethod
    def make_good_session(cls):
        good_sso_oauth_config_file = 'tests/config_files/sso_oauth_good.yaml'
        oauth_client_secret = cls.get_password('oauth_client_secret_good')

        s = cls.make_session(good_sso_oauth_config_file)
        s.set_oauth_client_secret(oauth_client_secret)
        return s

    @classmethod
    def remove_files(cls):
        os.remove('sso_oauth_cookie.txt')
        os.remove('token_file.npy')

    def test_get_incident(self):
        s = TestSessionSsoOauth.make_good_session()
        TestSessionBase.base_test_get_incident(self, s)
        TestSessionSsoOauth.remove_files()

    def test_insert_incident(self):
        s = TestSessionSsoOauth.make_good_session()
        TestSessionBase.base_test_insert_incident(self, s)
        TestSessionSsoOauth.remove_files()

    def test_update_incident(self):
        s = TestSessionSsoOauth.make_good_session()
        TestSessionBase.base_test_update_incident(self, s)
        TestSessionSsoOauth.remove_files()

    def test_session_persistance(self):
        s = TestSessionSsoOauth.make_good_session()
        TestSessionBase.base_test_session_persistance(self, s)
        TestSessionSsoOauth.remove_files()


if __name__ == '__main__':
    unittest.main()  # for compatibility with Python2.6 unittest
