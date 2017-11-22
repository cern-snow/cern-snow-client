# coding: utf-8

import unittest

from tests.test_base import TestBase
from tests.test_task_base import TestTaskBase


class TestTaskBasicAuthentication(unittest.TestCase, TestTaskBase):

    short_description_prefix = "snow client - task unit test - sso oauth"

    current_user = TestBase.sso_oauth_user

    @classmethod
    def make_good_session(cls):
        return cls.make_good_sso_oauth_session()

    @classmethod
    def remove_cookie(cls):
        cls.remove_sso_oauth_cookie_token_files()

    def test_task_get(self):
        s = self.make_good_session()
        TestTaskBase.base_test_task_get(self, s)
        self.remove_cookie()

    def test_task_insert(self):
        s = self.make_good_session()
        TestTaskBase.base_test_task_insert(self, s)
        self.remove_cookie()

    def test_task_update(self):
        s = self.make_good_session()
        TestTaskBase.base_test_task_update(self, s)
        self.remove_cookie()

    def test_add_comment(self):
        s = self.make_good_session()
        TestTaskBase.base_test_add_comment(self, s)
        self.remove_cookie()

    def test_add_work_note(self):
        s = self.make_good_session()
        TestTaskBase.base_test_add_work_note(self, s)
        self.remove_cookie()

    def test_take_in_progress(self):
        s = self.make_good_session()
        TestTaskBase.base_test_take_in_progress(self, s)
        self.remove_cookie()

    def test_resolve(self):
        s = self.make_good_session()
        TestTaskBase.base_test_resolve(self, s)
        self.remove_cookie()

    def test_task_query(self):
        s = self.make_good_session()
        TestTaskBase.base_test_task_query(self, s)
        self.remove_cookie()


if __name__ == '__main__':
    unittest.main()  # for compatibility with Python2.6 unittest
