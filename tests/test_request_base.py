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

from cern_snow_client.request import Request
from cern_snow_client.request import RequestQuery
from tests.test_base import TestBase


class TestRequestBase(TestBase):

    def base_test_request_get(self, s):
        req = Request(s)
        found = req.get('c69bd7324fdabac07db7d3ef0310c73b')
        self.assertTrue(found)
        self.assertEquals(req.sys_id, 'c69bd7324fdabac07db7d3ef0310c73b')
        self.assertEquals(req.number, 'RQF0746626')
        self.assertEquals(req.short_description, 'Test from Mats')
        self.assertEquals(req.get_table_name(), 'u_request_fulfillment')
        self.assertEquals(req.sys_class_name, 'u_request_fulfillment')
        self.assertEquals(req.u_current_task_state, '10')

        req = Request(s)
        found = req.get(('number', 'RQF0746626'))
        self.assertTrue(found)
        self.assertEquals(req.sys_id, 'c69bd7324fdabac07db7d3ef0310c73b')
        self.assertEquals(req.number, 'RQF0746626')
        self.assertEquals(req.short_description, 'Test from Mats')
        self.assertEquals(req.get_table_name(), 'u_request_fulfillment')
        self.assertEquals(req.sys_class_name, 'u_request_fulfillment')
        self.assertEquals(req.u_current_task_state, '10')

        req = Request(s)
        found = req.get(('number', 'INC0426232'))
        self.assertFalse(found)

    def base_test_request_insert(self, s):
        # request test with values in constructor
        req_original = Request(s, {
            'short_description': self.short_description_prefix + ' test_insert_request_1',
            'u_business_service': 'e85a3f3b0a0a8c0a006a2912f2f352d1',  # Service Element "ServiceNow"
            'u_functional_element': '579fb3d90a0a8c08017ac8a1137c8ee6',  # Functional Element "ServiceNow"
            'assignment_group': 'd34218f3b4a3a4006d2153f17c76edff',  # ServiceNow 4th line
            'comments': "Initial description"
        })
        self.assertTrue(req_original.get_can_insert())
        inserted = req_original.insert()
        self.assertTrue(inserted)
        self.assertTrue(req_original.sys_id is not None)
        self.assertEquals(req_original.get_table_name(), 'u_request_fulfillment')
        self.assertEquals(req_original.sys_class_name, 'u_request_fulfillment')
        self.assertEquals(req_original.short_description, self.short_description_prefix + ' test_insert_request_1')
        self.assertEquals(req_original.u_business_service, 'e85a3f3b0a0a8c0a006a2912f2f352d1')
        self.assertEquals(req_original.u_functional_element, '579fb3d90a0a8c08017ac8a1137c8ee6')
        self.assertEquals(req_original.assignment_group, 'd34218f3b4a3a4006d2153f17c76edff')
        self.assertEquals(req_original.description, 'Initial description')
        self.assertEquals(req_original.u_current_task_state, '2')

        req = Request(s)
        found = req.get(req_original.sys_id)
        self.assertTrue(found)

        self.assertEquals(req.sys_class_name, 'u_request_fulfillment')
        self.assertEquals(req.short_description, self.short_description_prefix + ' test_insert_request_1')
        self.assertEquals(req.u_business_service, 'e85a3f3b0a0a8c0a006a2912f2f352d1')
        self.assertEquals(req.u_functional_element, '579fb3d90a0a8c08017ac8a1137c8ee6')
        self.assertEquals(req.assignment_group, 'd34218f3b4a3a4006d2153f17c76edff')
        self.assertEquals(req.description, 'Initial description')
        self.assertEquals(req.u_current_task_state, '2')

        # request test, setting values after constructor
        req_original = Request(s)
        req_original.short_description = self.short_description_prefix + ' test_insert_request_2'
        req_original.u_business_service = 'e85a3f3b0a0a8c0a006a2912f2f352d1'  # Service Element "ServiceNow"
        req_original.u_functional_element = '579fb3d90a0a8c08017ac8a1137c8ee6'  # Functional Element "ServiceNow"
        req_original.assignment_group = 'd34218f3b4a3a4006d2153f17c76edff'  # ServiceNow 4th line
        req_original.comments = "Initial description"
        inserted = req_original.insert()
        self.assertTrue(req_original.get_can_insert())

        self.assertTrue(inserted)
        self.assertTrue(req_original.sys_id is not None)
        self.assertEquals(req_original.get_table_name(), 'u_request_fulfillment')
        self.assertEquals(req_original.sys_class_name, 'u_request_fulfillment')
        self.assertEquals(req_original.short_description, self.short_description_prefix + ' test_insert_request_2')
        self.assertEquals(req_original.u_business_service, 'e85a3f3b0a0a8c0a006a2912f2f352d1')
        self.assertEquals(req_original.u_functional_element, '579fb3d90a0a8c08017ac8a1137c8ee6')
        self.assertEquals(req_original.assignment_group, 'd34218f3b4a3a4006d2153f17c76edff')
        self.assertEquals(req_original.description, 'Initial description')
        self.assertEquals(req_original.u_current_task_state, '2')

        req = Request(s)
        found = req.get(req_original.sys_id)
        self.assertTrue(found)

        self.assertEquals(req.sys_class_name, 'u_request_fulfillment')
        self.assertEquals(req.number, req.number)
        self.assertEquals(req.short_description, self.short_description_prefix + ' test_insert_request_2')
        self.assertEquals(req.u_business_service, 'e85a3f3b0a0a8c0a006a2912f2f352d1')
        self.assertEquals(req.u_functional_element, '579fb3d90a0a8c08017ac8a1137c8ee6')
        self.assertEquals(req.assignment_group, 'd34218f3b4a3a4006d2153f17c76edff')
        self.assertEquals(req.description, 'Initial description')
        self.assertEquals(req.u_current_task_state, '2')

    def base_test_request_update(self, s):
        # insert a request for testing
        req_original = Request(s, {
            'short_description': self.short_description_prefix + ' test_update_request_1',
            'u_business_service': 'e85a3f3b0a0a8c0a006a2912f2f352d1',  # Service Element "ServiceNow"
            'u_functional_element': '579fb3d90a0a8c08017ac8a1137c8ee6',  # Functional Element "ServiceNow"
            'assignment_group': 'd34218f3b4a3a4006d2153f17c76edff',  # ServiceNow 4th line
            'comments': "Initial description"
        })
        inserted = req_original.insert()
        self.assertTrue(inserted)

        # get the request and the update it
        req = Request(s)
        found = req.get(req_original.sys_id)
        self.assertTrue(found)
        req.watch_list = 'test_watch_list_value@cern.ch'
        updated = req.update()
        self.assertTrue(updated)
        self.assertEquals(req.watch_list, 'test_watch_list_value@cern.ch')

        req = Request(s)
        found = req.get(req_original.sys_id)
        self.assertTrue(found)
        self.assertEquals(req.watch_list, 'test_watch_list_value@cern.ch')

        # update the request by sys_id without getting it
        req = Request(s)
        req.watch_list = 'test_watch_list_value_2@cern.ch'
        updated = req.update(req_original.sys_id)
        self.assertTrue(updated)
        self.assertEquals(req.watch_list, 'test_watch_list_value_2@cern.ch')

        req = Request(s)
        found = req.get(req_original.sys_id)
        self.assertTrue(found)
        self.assertEquals(req.watch_list, 'test_watch_list_value_2@cern.ch')

        # update the request by number without getting it
        req = Request(s)
        req.watch_list = 'test_watch_list_value_3@cern.ch'
        updated = req.update(('number', req_original.number))
        self.assertTrue(updated)
        self.assertEquals(req.watch_list, 'test_watch_list_value_3@cern.ch')

        req = Request(s)
        found = req.get(req_original.sys_id)
        self.assertTrue(found)
        self.assertEquals(req.watch_list, 'test_watch_list_value_3@cern.ch')

        # update the u_current_task_state after getting it
        req = Request(s)
        found = req.get(req_original.sys_id)
        self.assertTrue(found)
        req.u_current_task_state = '4'
        updated = req.update()
        self.assertTrue(updated)
        self.assertEquals(req.u_current_task_state, '4')

        req = Request(s)
        found = req.get(req_original.sys_id)
        self.assertTrue(found)
        self.assertEquals(req.u_current_task_state, '4')

        # update the u_current_task_state directly by sys_id
        req = Request(s)
        req.u_current_task_state = '5'
        updated = req.update(req_original.sys_id)
        self.assertTrue(updated)
        self.assertEquals(req.u_current_task_state, '5')

        req = Request(s)
        found = req.get(req_original.sys_id)
        self.assertTrue(found)
        self.assertEquals(req.u_current_task_state, '5')

        # update the u_current_task_state directly by number
        req = Request(s)
        req.u_current_task_state = '4'
        updated = req.update(('number', req_original.number))
        self.assertTrue(updated)
        self.assertEquals(req.u_current_task_state, '4')

        req = Request(s)
        found = req.get(req_original.sys_id)
        self.assertTrue(found)
        self.assertEquals(req.u_current_task_state, '4')

    def base_test_request_add_comment(self, s):
        req_original = Request(s, {  # s is a SnowRestSession object
            'short_description': self.short_description_prefix + ' test_request_add_comment',
            'u_business_service': 'e85a3f3b0a0a8c0a006a2912f2f352d1',  # Service Element "ServiceNow"
            'u_functional_element': '579fb3d90a0a8c08017ac8a1137c8ee6',  # Functional Element "ServiceNow"
            'assignment_group': 'd34218f3b4a3a4006d2153f17c76edff',  # ServiceNow 4th line
            'comments': "Initial description"
        })
        inserted = req_original.insert()
        self.assertTrue(inserted)

        req = Request(s)
        found = req.get(req_original.sys_id)
        self.assertTrue(found)

        updated = req.add_comment('New comment')
        self.assertTrue(updated)

        req = Request(s)
        updated = req.add_comment('New comment 2', req_original.sys_id)
        self.assertTrue(updated)

        req = Request(s)
        updated = req.add_comment('New comment 3', ('number', req_original.number))
        self.assertTrue(updated)

    def base_test_request_add_work_note(self, s):
        req_original = Request(s, {  # s is a SnowRestSession object
            'short_description': self.short_description_prefix + ' test_request_add_work_note',
            'u_business_service': 'e85a3f3b0a0a8c0a006a2912f2f352d1',  # Service Element "ServiceNow"
            'u_functional_element': '579fb3d90a0a8c08017ac8a1137c8ee6',  # Functional Element "ServiceNow"
            'assignment_group': 'd34218f3b4a3a4006d2153f17c76edff',  # ServiceNow 4th line
            'comments': "Initial description"
        })
        inserted = req_original.insert()
        self.assertTrue(inserted)

        req = Request(s)
        found = req.get(req_original.sys_id)
        self.assertTrue(found)

        updated = req.add_work_note('New work note')
        self.assertTrue(updated)

        req = Request(s)
        updated = req.add_work_note('New work note 2', req_original.sys_id)
        self.assertTrue(updated)

        req = Request(s)
        updated = req.add_work_note('New work note 3', ('number', req_original.number))
        self.assertTrue(updated)

    def base_test_request_take_in_progress(self, s):
        # first test: insert a request, get it, take it in progress
        r = Request(s, {  # s is a SnowRestSession object
            'short_description': self.short_description_prefix + ' test_request_take_in_progress',
            'u_business_service': 'e85a3f3b0a0a8c0a006a2912f2f352d1',  # Service Element "ServiceNow"
            'u_functional_element': '579fb3d90a0a8c08017ac8a1137c8ee6',  # Functional Element "ServiceNow"
            'assignment_group': 'd34218f3b4a3a4006d2153f17c76edff',  # ServiceNow 4th line
            'comments': "Initial description"
        })
        inserted = r.insert()
        self.assertTrue(inserted)

        t = Request(s)
        found = t.get(r.sys_id)
        self.assertTrue(found)

        updated = t.take_in_progress()
        self.assertTrue(updated)

        r2 = Request(s)
        found = r2.get(r.sys_id)
        self.assertTrue(found)
        self.assertTrue(r2.u_current_task_state, '4')
        self.assertTrue(r2.state, '2')
        self.assertTrue(r2.assigned_to, self.current_user)

        # second test: insert a request, take it in progress by providing the sys_id
        r = Request(s, {  # s is a SnowRestSession object
            'short_description': self.short_description_prefix + ' test_request_take_in_progress_2',
            'u_business_service': 'e85a3f3b0a0a8c0a006a2912f2f352d1',  # Service Element "ServiceNow"
            'u_functional_element': '579fb3d90a0a8c08017ac8a1137c8ee6',  # Functional Element "ServiceNow"
            'assignment_group': 'd34218f3b4a3a4006d2153f17c76edff',  # ServiceNow 4th line
            'comments': "Initial description"
        })
        inserted = r.insert()
        self.assertTrue(inserted)

        t = Request(s)
        updated = t.take_in_progress(key=r.sys_id)
        self.assertTrue(updated)

        r2 = Request(s)
        found = r2.get(r.sys_id)
        self.assertTrue(found)
        self.assertTrue(r2.u_current_task_state, '4')
        self.assertTrue(r2.state, '2')
        self.assertTrue(r2.assigned_to, self.current_user)

        # third test: insert a request, take it in progress by providing the number
        r = Request(s, {  # s is a SnowRestSession object
            'short_description': self.short_description_prefix + ' test_request_take_in_progress_3',
            'u_business_service': 'e85a3f3b0a0a8c0a006a2912f2f352d1',  # Service Element "ServiceNow"
            'u_functional_element': '579fb3d90a0a8c08017ac8a1137c8ee6',  # Functional Element "ServiceNow"
            'assignment_group': 'd34218f3b4a3a4006d2153f17c76edff',  # ServiceNow 4th line
            'comments': "Initial description"
        })
        inserted = r.insert()
        self.assertTrue(inserted)

        t = Request(s)
        updated = t.take_in_progress(key=('number', r.number))
        self.assertTrue(updated)

        r2 = Request(s)
        found = r2.get(r.sys_id)
        self.assertTrue(found)
        self.assertTrue(r2.u_current_task_state, '4')
        self.assertTrue(r2.state, '2')
        self.assertTrue(r2.assigned_to, self.current_user)

    def base_test_request_resolve(self, s):
        # first test: insert a request, get it, resolve it. No close code provided
        req_original = Request(s, {  # s is a SnowRestSession object
            'short_description': self.short_description_prefix + ' test_request_resolve',
            'u_business_service': 'e85a3f3b0a0a8c0a006a2912f2f352d1',  # Service Element "ServiceNow"
            'u_functional_element': '579fb3d90a0a8c08017ac8a1137c8ee6',  # Functional Element "ServiceNow"
            'assignment_group': 'd34218f3b4a3a4006d2153f17c76edff',  # ServiceNow 4th line
            'comments': "Initial description"
        })
        inserted = req_original.insert()
        self.assertTrue(inserted)

        req = Request(s)
        found = req.get(req_original.sys_id)
        self.assertTrue(found)

        updated = req.resolve('Solution text')
        self.assertTrue(updated)

        req = Request(s)
        found = req.get(req_original.sys_id)
        self.assertTrue(found)
        self.assertTrue(req.u_current_task_state, '9')
        self.assertTrue(req.state, '6')
        self.assertTrue(req.u_solution, 'Solution text')
        self.assertTrue(req.u_close_code, 'Restored')
        self.assertTrue(req.assigned_to, self.current_user)

        # second test: insert a request, resolve it providing the sys_id. No close code provided
        req_original = Request(s, {  # s is a SnowRestSession object
            'short_description': self.short_description_prefix + ' test_request_resolve_2',
            'u_business_service': 'e85a3f3b0a0a8c0a006a2912f2f352d1',  # Service Element "ServiceNow"
            'u_functional_element': '579fb3d90a0a8c08017ac8a1137c8ee6',  # Functional Element "ServiceNow"
            'assignment_group': 'd34218f3b4a3a4006d2153f17c76edff',  # ServiceNow 4th line
            'comments': "Initial description"
        })
        inserted = req_original.insert()
        self.assertTrue(inserted)

        req = Request(s)
        updated = req.resolve('Solution text', key=req_original.sys_id)
        self.assertTrue(updated)

        req = Request(s)
        found = req.get(req_original.sys_id)
        self.assertTrue(found)
        self.assertTrue(req.u_current_task_state, '9')
        self.assertTrue(req.state, '6')
        self.assertTrue(req.u_solution, 'Solution text')
        self.assertTrue(req.u_close_code, 'Restored')
        self.assertTrue(req.assigned_to, self.current_user)

        # third test: insert a request, resolve it providing the number. No close code provided
        req_original = Request(s, {  # s is a SnowRestSession object
            'short_description': self.short_description_prefix + ' test_request_resolve_3',
            'u_business_service': 'e85a3f3b0a0a8c0a006a2912f2f352d1',  # Service Element "ServiceNow"
            'u_functional_element': '579fb3d90a0a8c08017ac8a1137c8ee6',  # Functional Element "ServiceNow"
            'assignment_group': 'd34218f3b4a3a4006d2153f17c76edff',  # ServiceNow 4th line
            'comments': "Initial description"
        })
        inserted = req_original.insert()
        self.assertTrue(inserted)

        req = Request(s)
        updated = req.resolve('Solution text', key=('number', req_original.number))
        self.assertTrue(updated)

        req = Request(s)
        found = req.get(req_original.sys_id)
        self.assertTrue(found)
        self.assertTrue(req.u_current_task_state, '9')
        self.assertTrue(req.state, '6')
        self.assertTrue(req.u_solution, 'Solution text')
        self.assertTrue(req.u_close_code, 'Restored')
        self.assertTrue(req.assigned_to, self.current_user)

        # fourth test: insert a request, get it, resolve ireq. Provide a non-default close code
        req_original = Request(s, {  # s is a SnowRestSession object
            'short_description': self.short_description_prefix + ' test_request_resolve_4',
            'u_business_service': 'e85a3f3b0a0a8c0a006a2912f2f352d1',  # Service Element "ServiceNow"
            'u_functional_element': '579fb3d90a0a8c08017ac8a1137c8ee6',  # Functional Element "ServiceNow"
            'assignment_group': 'd34218f3b4a3a4006d2153f17c76edff',  # ServiceNow 4th line
            'comments': "Initial description"
        })
        inserted = req_original.insert()
        self.assertTrue(inserted)

        req = Request(s)
        found = req.get(req_original.sys_id)
        self.assertTrue(found)

        updated = req.resolve('Solution text', 'Not authorised')
        self.assertTrue(updated)

        req = Request(s)
        found = req.get(req_original.sys_id)
        self.assertTrue(found)
        self.assertTrue(req.u_current_task_state, '9')
        self.assertTrue(req.state, '6')
        self.assertTrue(req.u_solution, 'Solution text')
        self.assertTrue(req.u_close_code, 'Not authorised')
        self.assertTrue(req.assigned_to, self.current_user)

    def base_test_request_query(self, s):
        req = RequestQuery(s)

        # Query the requests with FE=IT Service Management Support,
        # Visibility=CERN, Created in 2016, and already closed
        record_set = req.query(query_filter={
            'u_functional_element': 'ea56fb210a0a8c0a015a591ddbed3676',
            'u_visibility': 'cern',
            'active': 'false'
        })

        records_found = False
        for record in record_set:
            records_found = True
            self.assertTrue(bool(record.number))
            self.assertTrue(bool(record.short_description))
            self.assertEquals(record.sys_class_name, 'u_request_fulfillment')
            self.assertTrue(type(record) is Request)
            self.assertTrue(hasattr(record, 'u_current_task_state'))

        self.assertTrue(records_found)

        req = RequestQuery(s)

        # Query the requests with FE=IT Service Management Support,
        # Visibility=CERN, Created in 2016, and already closed
        record_set = req.query(
            query_encoded="u_functional_element=ea56fb210a0a8c0a015a591ddbed3676^u_visibility=cern^active=false^"
                          "sys_created_onDATEPART2016@javascript:gs.datePart('year','2016','EE')")

        records_found = False
        for record in record_set:
            records_found = True
            self.assertTrue(bool(record.number))
            self.assertTrue(bool(record.short_description))
            self.assertEquals(record.sys_class_name, 'u_request_fulfillment')
            self.assertTrue(type(record) is Request)
            self.assertTrue(hasattr(record, 'u_current_task_state'))

        self.assertTrue(records_found)
