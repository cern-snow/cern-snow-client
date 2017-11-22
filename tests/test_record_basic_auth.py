# coding: utf-8

import unittest

from tests.test_base import TestBase
from tests.test_record_base import TestRecordBase


class TestRecordBasicAuthentication(unittest.TestCase, TestRecordBase):

    short_description_prefix = "snow client - record unit test - basic auth"

    current_user = TestBase.basic_auth_user

    @classmethod
    def make_good_session(cls):
        return cls.make_good_basic_auth_session()

    @classmethod
    def remove_cookie(cls):
        cls.remove_basic_cookie_file()

    def test_get_record(self):
        s = self.make_good_session()
        TestRecordBase.base_test_get_record(self, s)
        self.remove_cookie()

    def test_insert_record(self):
        s = self.make_good_session()
        TestRecordBase.base_test_insert_record(self, s)
        self.remove_cookie()

    def test_update_record(self):
        s = self.make_good_session()
        TestRecordBase.base_test_update_record(self, s)
        self.remove_cookie()

    def test_record_query(self):
        s = self.make_good_session()
        TestRecordBase.base_test_get_query(self, s)
        self.remove_cookie()


if __name__ == '__main__':
    unittest.main()  # for compatibility with Python2.6 unittest
