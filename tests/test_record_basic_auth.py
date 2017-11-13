# coding: utf-8

import unittest
import os

from tests.test_record_base import TestRecordBase


class TestRecordBasicAuthentication(unittest.TestCase, TestRecordBase):

    short_description_prefix = "snow client - record unit test - basic auth"

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


if __name__ == '__main__':
    unittest.main()  # for compatibility with Python2.6 unittest
