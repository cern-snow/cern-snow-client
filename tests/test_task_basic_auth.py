# coding: utf-8

import unittest

from tests.test_base import TestBase
from tests.test_task_base import TestTaskBase


class TestTaskBasicAuthentication(unittest.TestCase, TestTaskBase):

    short_description_prefix = "snow client - task unit test - basic auth"

    current_user = TestBase.basic_auth_user

    @classmethod
    def make_good_session(cls):
        return cls.make_good_basic_auth_session()

    @classmethod
    def remove_cookie(cls):
        cls.remove_basic_cookie_file()

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

    def test_task_get_by_number(self):
        s = self.make_good_session()
        TestTaskBase.base_task_get_by_number(self, s)
        self.remove_cookie()


if __name__ == '__main__':
    unittest.main()  # for compatibility with Python2.6 unittest
