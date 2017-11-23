# coding: utf-8

import unittest

from tests.test_base import TestBase
from tests.test_request_base import TestRequestBase


class TestIncidentBasicAuthentication(unittest.TestCase, TestRequestBase):

    short_description_prefix = "snow client - request unit test - basic auth"

    current_user = TestBase.basic_auth_user

    @classmethod
    def make_good_session(cls):
        return cls.make_good_basic_auth_session()

    @classmethod
    def remove_cookie(cls):
        cls.remove_basic_cookie_file()

    def test_request_get(self):
        s = self.make_good_session()
        TestRequestBase.base_test_request_get(self, s)
        self.remove_cookie()

    def test_request_insert(self):
        s = self.make_good_session()
        TestRequestBase.base_test_request_insert(self, s)
        self.remove_cookie()

    def test_request_update(self):
        s = self.make_good_session()
        TestRequestBase.base_test_request_update(self, s)
        self.remove_cookie()

    def test_request_add_comment(self):
        s = self.make_good_session()
        TestRequestBase.base_test_request_add_comment(self, s)
        self.remove_cookie()

    def test_request_add_work_note(self):
        s = self.make_good_session()
        TestRequestBase.base_test_request_add_work_note(self, s)
        self.remove_cookie()

    def test_request_take_in_progress(self):
        s = self.make_good_session()
        TestRequestBase.base_test_request_take_in_progress(self, s)
        self.remove_cookie()

    def test_request_resolve(self):
        s = self.make_good_session()
        TestRequestBase.base_test_request_resolve(self, s)
        self.remove_cookie()

    def test_request_query(self):
        s = self.make_good_session()
        TestRequestBase.base_test_request_query(self, s)
        self.remove_cookie()


if __name__ == '__main__':
    unittest.main()  # for compatibility with Python2.6 unittest
