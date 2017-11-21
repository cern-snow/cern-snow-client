# coding: utf-8

import unittest
import os

from tests.test_session_base import TestSessionBase


class TestSessionBasicAuthentication(unittest.TestCase, TestSessionBase):

    short_description_prefix = "snow client - session unit test - basic auth"

    @classmethod
    def make_good_session(cls):
        good_basic_auth_config_file = 'tests/config_files/basic_good.yaml'
        basic_auth_password = cls.get_password('basic_good')

        s = cls.make_session(good_basic_auth_config_file)
        s.set_basic_auth_password(basic_auth_password)
        return s

    @classmethod
    def remove_cookie(cls):
        os.remove('basic_cookie.txt')

    def test_get(self):
        s = self.make_good_session()
        TestSessionBase.base_test_get(self, s)
        self.remove_cookie()

    def test_post(self):
        s = self.make_good_session()
        TestSessionBase.base_test_post(self, s)
        self.remove_cookie()

    def test_put(self):
        s = self.make_good_session()
        TestSessionBase.base_test_put(self, s)
        self.remove_cookie()

    def test_session_persistance(self):
        s = self.make_good_session()
        TestSessionBase.base_test_session_persistance(self, s)
        self.remove_cookie()


if __name__ == '__main__':
    unittest.main()  # for compatibility with Python2.6 unittest
