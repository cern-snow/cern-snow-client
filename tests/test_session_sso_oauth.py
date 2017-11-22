# coding: utf-8

import unittest

from tests.test_session_base import TestSessionBase


class TestSessionSsoOauth(unittest.TestCase, TestSessionBase):

    short_description_prefix = "snow client - session unit test - sso oauth"

    @classmethod
    def make_good_session(cls):
        return cls.make_good_sso_oauth_session()

    @classmethod
    def remove_files(cls):
        cls.remove_sso_oauth_cookie_token_files()

    def test_get(self):
        s = self.make_good_session()
        TestSessionBase.base_test_get(self, s)
        self.remove_files()

    def test_post(self):
        s = self.make_good_session()
        TestSessionBase.base_test_post(self, s)
        self.remove_files()

    def test_put(self):
        s = self.make_good_session()
        TestSessionBase.base_test_put(self, s)
        self.remove_files()

    def test_session_persistance(self):
        s = self.make_good_session()
        TestSessionBase.base_test_session_persistance(self, s)
        self.remove_files()


if __name__ == '__main__':
    unittest.main()  # for compatibility with Python2.6 unittest
