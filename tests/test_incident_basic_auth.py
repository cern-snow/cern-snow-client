# -*- coding: utf-8 -*-
#
# This file is part of the cern-snow-client library.
# Copyright (c) 2017 CERN
# Authors:
#  - James Clerc <james.clerc@cern.ch> <james.clerc@epitech.eu>
#  - David Martin Clavo <david.martin.clavo@cern.ch>
#
# The cern-snow-client library is free software; you can redistribute it
# and/or modify it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
#
# The cern-snow-client library is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
# without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with the cern-snow-client library.  If not, see <http://www.gnu.org/licenses/>.
#
# In applying this license, CERN does not waive the privileges and immunities granted to it by virtue of its status
# as an Intergovernmental Organization or submit itself to any jurisdiction.

import unittest

from tests.test_base import TestBase
from tests.test_incident_base import TestIncidentBase


class TestIncidentBasicAuthentication(unittest.TestCase, TestIncidentBase):

    short_description_prefix = "snow client - incident unit test - basic auth"

    current_user = TestBase.basic_auth_user

    @classmethod
    def make_good_session(cls):
        return cls.make_good_basic_auth_session()

    @classmethod
    def remove_cookie(cls):
        cls.remove_basic_cookie_file()

    def test_incident_get(self):
        s = self.make_good_session()
        TestIncidentBase.base_test_incident_get(self, s)
        self.remove_cookie()

    def test_incident_insert(self):
        s = self.make_good_session()
        TestIncidentBase.base_test_incident_insert(self, s)
        self.remove_cookie()

    def test_incident_update(self):
        s = self.make_good_session()
        TestIncidentBase.base_test_incident_update(self, s)
        self.remove_cookie()

    def test_incident_add_comment(self):
        s = self.make_good_session()
        TestIncidentBase.base_test_incident_add_comment(self, s)
        self.remove_cookie()

    def test_incident_add_work_note(self):
        s = self.make_good_session()
        TestIncidentBase.base_test_incident_add_work_note(self, s)
        self.remove_cookie()

    def test_incident_take_in_progress(self):
        s = self.make_good_session()
        TestIncidentBase.base_test_incident_take_in_progress(self, s)
        self.remove_cookie()

    def test_incident_resolve(self):
        s = self.make_good_session()
        TestIncidentBase.base_test_incident_resolve(self, s)
        self.remove_cookie()

    def test_incident_query(self):
        s = self.make_good_session()
        TestIncidentBase.base_test_incident_query(self, s)
        self.remove_cookie()


if __name__ == '__main__':
    unittest.main()  # for compatibility with Python2.6 unittest
