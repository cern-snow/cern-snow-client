# -*- coding: utf-8 -*-
#
# This file is part of the cern-snow-client library.
# Copyright (c) 2017 CERN
# Authors: James Clerc <james.clerc@cern.ch>, David Martin Clavo <david.martin.clavo@cern.ch>
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

from cern_snow_client.record import Record
from cern_snow_client.task import Task
from cern_snow_client.task import TaskQuery
from cern_snow_client.incident import Incident
from tests.test_base import TestBase
from cern_snow_client.common import SnowClientException


class TestTaskBase(TestBase):

    def base_test_task_get(self, s):
        t = Task(s)
        found = t.get('c1c535ba85f45540adf94de5b835cd43')
        self.assertTrue(found)
        self.assertEquals(t.sys_id, 'c1c535ba85f45540adf94de5b835cd43')
        self.assertEquals(t.number, 'INC0426232')
        self.assertEquals(t.short_description, 'Test')
        self.assertEquals(t.get_table_name(), 'task')
        self.assertEquals(t.sys_class_name, 'incident')
        self.assertTrue(not hasattr(t, 'incident_state'))

        t = Task(s)
        found = t.get(('number', 'INC0426232'))
        self.assertTrue(found)
        self.assertEquals(t.sys_id, 'c1c535ba85f45540adf94de5b835cd43')
        self.assertEquals(t.number, 'INC0426232')
        self.assertEquals(t.short_description, 'Test')
        self.assertEquals(t.get_table_name(), 'task')
        self.assertEquals(t.sys_class_name, 'incident')
        self.assertTrue(not hasattr(t, 'incident_state'))

        t = Task(s)
        found = t.get('c69bd7324fdabac07db7d3ef0310c73b')
        self.assertTrue(found)
        self.assertEquals(t.sys_id, 'c69bd7324fdabac07db7d3ef0310c73b')
        self.assertEquals(t.number, 'RQF0746626')
        self.assertEquals(t.short_description, 'Test from Mats')
        self.assertEquals(t.get_table_name(), 'task')
        self.assertEquals(t.sys_class_name, 'u_request_fulfillment')
        self.assertTrue(not hasattr(t, 'u_current_task_state'))

        t = Task(s)
        found = t.get(('number', 'RQF0746626'))
        self.assertTrue(found)
        self.assertEquals(t.sys_id, 'c69bd7324fdabac07db7d3ef0310c73b')
        self.assertEquals(t.number, 'RQF0746626')
        self.assertEquals(t.short_description, 'Test from Mats')
        self.assertEquals(t.get_table_name(), 'task')
        self.assertEquals(t.sys_class_name, 'u_request_fulfillment')
        self.assertTrue(not hasattr(t, 'u_current_task_state'))

        t = Task(s, 'incident')
        found = t.get('c1c535ba85f45540adf94de5b835cd43')
        self.assertTrue(found)
        self.assertEquals(t.sys_id, 'c1c535ba85f45540adf94de5b835cd43')
        self.assertEquals(t.number, 'INC0426232')
        self.assertEquals(t.short_description, 'Test')
        self.assertEquals(t.get_table_name(), 'incident')
        self.assertEquals(t.sys_class_name, 'incident')
        self.assertTrue(hasattr(t, 'incident_state'))
        self.assertEquals(t.incident_state, '7')

        t = Task(s, 'incident')
        found = t.get(('number', 'RQF0746626'))
        self.assertFalse(found)

    def base_test_task_insert(self, s):
        # incident test
        t = Task(s, 'incident', {
            'short_description': self.short_description_prefix + ' test_insert_task_1',
            'u_business_service': 'e85a3f3b0a0a8c0a006a2912f2f352d1',  # Service Element "ServiceNow"
            'u_functional_element': '579fb3d90a0a8c08017ac8a1137c8ee6',  # Functional Element "ServiceNow"
            'assignment_group': 'd34218f3b4a3a4006d2153f17c76edff',  # ServiceNow 4th line
            'comments': "Initial description"
        })
        self.assertTrue(t.get_can_insert())
        inserted = t.insert()
        self.assertTrue(inserted)
        self.assertTrue(t.sys_id is not None)
        self.assertEquals(t.get_table_name(), 'incident')
        self.assertEquals(t.sys_class_name, 'incident')
        self.assertEquals(t.short_description, self.short_description_prefix + ' test_insert_task_1')
        self.assertEquals(t.u_business_service, 'e85a3f3b0a0a8c0a006a2912f2f352d1')
        self.assertEquals(t.u_functional_element, '579fb3d90a0a8c08017ac8a1137c8ee6')
        self.assertEquals(t.assignment_group, 'd34218f3b4a3a4006d2153f17c76edff')
        self.assertEquals(t.description, 'Initial description')
        self.assertEquals(t.incident_state, '2')

        r = Record(s, 'incident')
        found = r.get(t.sys_id)
        self.assertTrue(found)

        self.assertEquals(r.sys_class_name, 'incident')
        self.assertEquals(r.short_description, self.short_description_prefix + ' test_insert_task_1')
        self.assertEquals(r.u_business_service, 'e85a3f3b0a0a8c0a006a2912f2f352d1')
        self.assertEquals(r.u_functional_element, '579fb3d90a0a8c08017ac8a1137c8ee6')
        self.assertEquals(r.assignment_group, 'd34218f3b4a3a4006d2153f17c76edff')
        self.assertEquals(r.description, 'Initial description')
        self.assertEquals(r.incident_state, '2')

        # request test
        t = Task(s, 'u_request_fulfillment')
        t.short_description = self.short_description_prefix + ' test_insert_task_2'
        t.u_business_service = 'e85a3f3b0a0a8c0a006a2912f2f352d1'  # Service Element "ServiceNow"
        t.u_functional_element = '579fb3d90a0a8c08017ac8a1137c8ee6'  # Functional Element "ServiceNow"
        t.assignment_group = 'd34218f3b4a3a4006d2153f17c76edff'  # ServiceNow 4th line
        t.comments = "Initial description"
        inserted = t.insert()
        self.assertTrue(t.get_can_insert())

        self.assertTrue(inserted)
        self.assertTrue(t.sys_id is not None)
        self.assertEquals(t.get_table_name(), 'u_request_fulfillment')
        self.assertEquals(t.sys_class_name, 'u_request_fulfillment')
        self.assertEquals(t.short_description, self.short_description_prefix + ' test_insert_task_2')
        self.assertEquals(t.u_business_service, 'e85a3f3b0a0a8c0a006a2912f2f352d1')
        self.assertEquals(t.u_functional_element, '579fb3d90a0a8c08017ac8a1137c8ee6')
        self.assertEquals(t.assignment_group, 'd34218f3b4a3a4006d2153f17c76edff')
        self.assertEquals(t.description, 'Initial description')
        self.assertEquals(t.u_current_task_state, '2')

        r = Record(s, 'u_request_fulfillment')
        found = r.get(t.sys_id)
        self.assertTrue(found)

        self.assertEquals(r.sys_class_name, 'u_request_fulfillment')
        self.assertEquals(r.short_description, self.short_description_prefix + ' test_insert_task_2')
        self.assertEquals(r.u_business_service, 'e85a3f3b0a0a8c0a006a2912f2f352d1')
        self.assertEquals(r.u_functional_element, '579fb3d90a0a8c08017ac8a1137c8ee6')
        self.assertEquals(r.assignment_group, 'd34218f3b4a3a4006d2153f17c76edff')
        self.assertEquals(r.description, 'Initial description')
        self.assertEquals(r.u_current_task_state, '2')

        # insertion without specifying table test
        t = Task(s)
        self.assertFalse(t.get_can_insert())
        self.assertRaises(SnowClientException, Task.insert, t)

    def base_test_task_update(self, s):
        # insert an incident for testing
        t_original = Task(s, 'incident', {
            'short_description': self.short_description_prefix + ' test_update_task_1',
            'u_business_service': 'e85a3f3b0a0a8c0a006a2912f2f352d1',  # Service Element "ServiceNow"
            'u_functional_element': '579fb3d90a0a8c08017ac8a1137c8ee6',  # Functional Element "ServiceNow"
            'assignment_group': 'd34218f3b4a3a4006d2153f17c76edff',  # ServiceNow 4th line
            'comments': "Initial description"
        })
        inserted = t_original.insert()
        self.assertTrue(inserted)

        # get the incident and the update it
        t = Task(s)
        found = t.get(t_original.sys_id)
        self.assertTrue(found)
        t.watch_list = 'test_watch_list_value@cern.ch'
        updated = t.update()
        self.assertTrue(updated)
        self.assertEquals(t.watch_list, 'test_watch_list_value@cern.ch')

        t = Task(s)
        found = t.get(t_original.sys_id)
        self.assertTrue(found)
        self.assertEquals(t.watch_list, 'test_watch_list_value@cern.ch')

        # update the incident by sys_id without getting it
        t = Task(s)
        t.watch_list = 'test_watch_list_value_2@cern.ch'
        updated = t.update(t_original.sys_id)
        self.assertTrue(updated)
        self.assertEquals(t.watch_list, 'test_watch_list_value_2@cern.ch')

        t = Task(s)
        found = t.get(t_original.sys_id)
        self.assertTrue(found)
        self.assertEquals(t.watch_list, 'test_watch_list_value_2@cern.ch')

        # update the incident by number without getting it
        t = Task(s)
        t.watch_list = 'test_watch_list_value_3@cern.ch'
        updated = t.update(('number', t_original.number))
        self.assertTrue(updated)
        self.assertEquals(t.watch_list, 'test_watch_list_value_3@cern.ch')

        t = Task(s)
        found = t.get(t_original.sys_id)
        self.assertTrue(found)
        self.assertEquals(t.watch_list, 'test_watch_list_value_3@cern.ch')

        # update the incident_state after getting it
        t = Task(s, 'incident')
        found = t.get(t_original.sys_id)
        self.assertTrue(found)
        t.incident_state = '3'
        updated = t.update()
        self.assertTrue(updated)
        self.assertEquals(t.incident_state, '3')

        t = Task(s, 'incident')
        found = t.get(t_original.sys_id)
        self.assertTrue(found)
        self.assertEquals(t.incident_state, '3')

        # update the incident_state directly by sys_id
        t = Task(s, 'incident')
        t.incident_state = '4'
        updated = t.update(t_original.sys_id)
        self.assertTrue(updated)
        self.assertEquals(t.incident_state, '4')

        t = Task(s, 'incident')
        found = t.get(t_original.sys_id)
        self.assertTrue(found)
        self.assertEquals(t.incident_state, '4')

        # update the incident_state directly by number
        t = Task(s, 'incident')
        t.incident_state = '3'
        updated = t.update(('number', t_original.number))
        self.assertTrue(updated)
        self.assertEquals(t.incident_state, '3')

        t = Task(s, 'incident')
        found = t.get(t_original.sys_id)
        self.assertTrue(found)
        self.assertEquals(t.incident_state, '3')

        # same 3 tests but without providing a table
        t = Task(s)
        found = t.get(t_original.sys_id)
        self.assertTrue(found)
        t.incident_state = '2'
        updated = t.update()
        self.assertTrue(updated)
        self.assertEquals(t.incident_state, '2')

        t = Task(s, 'incident')
        found = t.get(t_original.sys_id)
        self.assertTrue(found)
        self.assertEquals(t.incident_state, '2')

        t = Task(s)
        t.incident_state = '3'
        updated = t.update(t_original.sys_id)
        self.assertTrue(updated)
        self.assertEquals(t.incident_state, '3')

        t = Task(s, 'incident')
        found = t.get(t_original.sys_id)
        self.assertTrue(found)
        self.assertEquals(t.incident_state, '3')

        t = Task(s)
        t.incident_state = '4'
        updated = t.update(('number', t_original.number))
        self.assertTrue(updated)
        self.assertEquals(t.incident_state, '4')

        t = Task(s, 'incident')
        found = t.get(t_original.sys_id)
        self.assertTrue(found)
        self.assertEquals(t.incident_state, '4')

        # providing a wrong table
        t = Task(s, 'u_request_fulfillment')
        t.incident_state = '2'
        updated = t.update(t_original.sys_id)
        self.assertFalse(updated)

    def base_test_add_comment(self, s):
        r = Record(s, 'incident', {  # s is a SnowRestSession object
            'short_description': self.short_description_prefix + ' test_add_comment',
            'u_business_service': 'e85a3f3b0a0a8c0a006a2912f2f352d1',  # Service Element "ServiceNow"
            'u_functional_element': '579fb3d90a0a8c08017ac8a1137c8ee6',  # Functional Element "ServiceNow"
            'assignment_group': 'd34218f3b4a3a4006d2153f17c76edff',  # ServiceNow 4th line
            'comments': "Initial description"
        })
        inserted = r.insert()
        self.assertTrue(inserted)

        t = Task(s)
        found = t.get(r.sys_id)
        self.assertTrue(found)

        updated = t.add_comment('New comment')
        self.assertTrue(updated)

        t2 = Task(s)
        updated = t2.add_comment('New comment 2', r.sys_id)
        self.assertTrue(updated)

        t3 = Task(s)
        updated = t3.add_comment('New comment 3', ('number', r.number))
        self.assertTrue(updated)

    def base_test_add_work_note(self, s):
        r = Record(s, 'incident', {  # s is a SnowRestSession object
            'short_description': self.short_description_prefix + ' test_add_work_note',
            'u_business_service': 'e85a3f3b0a0a8c0a006a2912f2f352d1',  # Service Element "ServiceNow"
            'u_functional_element': '579fb3d90a0a8c08017ac8a1137c8ee6',  # Functional Element "ServiceNow"
            'assignment_group': 'd34218f3b4a3a4006d2153f17c76edff',  # ServiceNow 4th line
            'comments': "Initial description"
        })
        inserted = r.insert()
        self.assertTrue(inserted)

        t = Task(s)
        found = t.get(r.sys_id)
        self.assertTrue(found)

        updated = t.add_work_note('New work note')
        self.assertTrue(updated)

        t2 = Task(s)
        updated = t2.add_work_note('New work note 2', r.sys_id)
        self.assertTrue(updated)

        t3 = Task(s)
        updated = t3.add_work_note('New work note 3', ('number', r.number))
        self.assertTrue(updated)

    def base_test_take_in_progress(self, s):
        # first test: insert an incident, get it, take it in progress
        r = Record(s, 'incident', {  # s is a SnowRestSession object
            'short_description': self.short_description_prefix + ' test_take_in_progress',
            'u_business_service': 'e85a3f3b0a0a8c0a006a2912f2f352d1',  # Service Element "ServiceNow"
            'u_functional_element': '579fb3d90a0a8c08017ac8a1137c8ee6',  # Functional Element "ServiceNow"
            'assignment_group': 'd34218f3b4a3a4006d2153f17c76edff',  # ServiceNow 4th line
            'comments': "Initial description"
        })
        inserted = r.insert()
        self.assertTrue(inserted)

        t = Task(s)
        found = t.get(r.sys_id)
        self.assertTrue(found)

        updated = t.take_in_progress()
        self.assertTrue(updated)

        r2 = Record(s, 'incident')
        found = r2.get(r.sys_id)
        self.assertTrue(found)
        self.assertTrue(r2.incident_state, '3')
        self.assertTrue(r2.state, '2')
        self.assertTrue(r2.assigned_to, self.current_user)

        # second test: insert an incident, take it in progress by providing the sys_id
        r = Record(s, 'incident', {  # s is a SnowRestSession object
            'short_description': self.short_description_prefix + ' test_take_in_progress_2',
            'u_business_service': 'e85a3f3b0a0a8c0a006a2912f2f352d1',  # Service Element "ServiceNow"
            'u_functional_element': '579fb3d90a0a8c08017ac8a1137c8ee6',  # Functional Element "ServiceNow"
            'assignment_group': 'd34218f3b4a3a4006d2153f17c76edff',  # ServiceNow 4th line
            'comments': "Initial description"
        })
        inserted = r.insert()
        self.assertTrue(inserted)

        t = Task(s)
        updated = t.take_in_progress(key=r.sys_id)
        self.assertTrue(updated)

        r2 = Record(s, 'incident')
        found = r2.get(r.sys_id)
        self.assertTrue(found)
        self.assertTrue(r2.incident_state, '3')
        self.assertTrue(r2.state, '2')
        self.assertTrue(r2.assigned_to, self.current_user)

        # third test: insert an incident, take it in progress by providing the number
        r = Record(s, 'incident', {  # s is a SnowRestSession object
            'short_description': self.short_description_prefix + ' test_take_in_progress_3',
            'u_business_service': 'e85a3f3b0a0a8c0a006a2912f2f352d1',  # Service Element "ServiceNow"
            'u_functional_element': '579fb3d90a0a8c08017ac8a1137c8ee6',  # Functional Element "ServiceNow"
            'assignment_group': 'd34218f3b4a3a4006d2153f17c76edff',  # ServiceNow 4th line
            'comments': "Initial description"
        })
        inserted = r.insert()
        self.assertTrue(inserted)

        t = Task(s)
        updated = t.take_in_progress(key=('number', r.number))
        self.assertTrue(updated)

        r2 = Record(s, 'incident')
        found = r2.get(r.sys_id)
        self.assertTrue(found)
        self.assertTrue(r2.incident_state, '3')
        self.assertTrue(r2.state, '2')
        self.assertTrue(r2.assigned_to, self.current_user)

        # fourth test: insert a request, get it, take it in progress
        r = Record(s, 'u_request_fulfillment', {  # s is a SnowRestSession object
            'short_description': self.short_description_prefix + ' test_take_in_progress_4',
            'u_business_service': 'e85a3f3b0a0a8c0a006a2912f2f352d1',  # Service Element "ServiceNow"
            'u_functional_element': '579fb3d90a0a8c08017ac8a1137c8ee6',  # Functional Element "ServiceNow"
            'assignment_group': 'd34218f3b4a3a4006d2153f17c76edff',  # ServiceNow 4th line
            'comments': "Initial description"
        })
        inserted = r.insert()
        self.assertTrue(inserted)

        t = Task(s)
        found = t.get(r.sys_id)
        self.assertTrue(found)

        updated = t.take_in_progress()
        self.assertTrue(updated)

        r2 = Record(s, 'u_request_fulfillment')
        found = r2.get(r.sys_id)
        self.assertTrue(found)
        self.assertTrue(r2.u_current_task_state, '4')
        self.assertTrue(r2.state, '2')
        self.assertTrue(r2.assigned_to, self.current_user)

        # fifth test: insert an request, take it in progress by providing the sys_id
        r = Record(s, 'u_request_fulfillment', {  # s is a SnowRestSession object
            'short_description': self.short_description_prefix + ' test_take_in_progress_5',
            'u_business_service': 'e85a3f3b0a0a8c0a006a2912f2f352d1',  # Service Element "ServiceNow"
            'u_functional_element': '579fb3d90a0a8c08017ac8a1137c8ee6',  # Functional Element "ServiceNow"
            'assignment_group': 'd34218f3b4a3a4006d2153f17c76edff',  # ServiceNow 4th line
            'comments': "Initial description"
        })
        inserted = r.insert()
        self.assertTrue(inserted)

        t = Task(s)
        updated = t.take_in_progress(key=r.sys_id)
        self.assertTrue(updated)

        r2 = Record(s, 'u_request_fulfillment')
        found = r2.get(r.sys_id)
        self.assertTrue(found)
        self.assertTrue(r2.u_current_task_state, '4')
        self.assertTrue(r2.state, '2')
        self.assertTrue(r2.assigned_to, self.current_user)

        # sixth test: insert an request, take it in progress by providing the number
        r = Record(s, 'u_request_fulfillment', {  # s is a SnowRestSession object
            'short_description': self.short_description_prefix + ' test_take_in_progress_6',
            'u_business_service': 'e85a3f3b0a0a8c0a006a2912f2f352d1',  # Service Element "ServiceNow"
            'u_functional_element': '579fb3d90a0a8c08017ac8a1137c8ee6',  # Functional Element "ServiceNow"
            'assignment_group': 'd34218f3b4a3a4006d2153f17c76edff',  # ServiceNow 4th line
            'comments': "Initial description"
        })
        inserted = r.insert()
        self.assertTrue(inserted)

        t = Task(s)
        updated = t.take_in_progress(key=('number', r.number))
        self.assertTrue(updated)

        r2 = Record(s, 'u_request_fulfillment')
        found = r2.get(r.sys_id)
        self.assertTrue(found)
        self.assertTrue(r2.u_current_task_state, '4')
        self.assertTrue(r2.state, '2')
        self.assertTrue(r2.assigned_to, self.current_user)

    def base_test_resolve(self, s):
        # first test: insert an incident, get it, resolve it. No close code provided
        r = Record(s, 'incident', {  # s is a SnowRestSession object
            'short_description': self.short_description_prefix + ' test_resolve',
            'u_business_service': 'e85a3f3b0a0a8c0a006a2912f2f352d1',  # Service Element "ServiceNow"
            'u_functional_element': '579fb3d90a0a8c08017ac8a1137c8ee6',  # Functional Element "ServiceNow"
            'assignment_group': 'd34218f3b4a3a4006d2153f17c76edff',  # ServiceNow 4th line
            'comments': "Initial description"
        })
        inserted = r.insert()
        self.assertTrue(inserted)

        t = Task(s)
        found = t.get(r.sys_id)
        self.assertTrue(found)

        updated = t.resolve('Solution text')
        self.assertTrue(updated)

        r2 = Record(s, 'incident')
        found = r2.get(r.sys_id)
        self.assertTrue(found)
        self.assertTrue(r2.incident_state, '6')
        self.assertTrue(r2.state, '6')
        self.assertTrue(r2.u_solution, 'Solution text')
        self.assertTrue(r2.u_close_code, 'Restored')
        self.assertTrue(r2.assigned_to, self.current_user)

        # second test: insert an incident, resolve it providing the sys_id. No close code provided
        r = Record(s, 'incident', {  # s is a SnowRestSession object
            'short_description': self.short_description_prefix + ' test_resolve_2',
            'u_business_service': 'e85a3f3b0a0a8c0a006a2912f2f352d1',  # Service Element "ServiceNow"
            'u_functional_element': '579fb3d90a0a8c08017ac8a1137c8ee6',  # Functional Element "ServiceNow"
            'assignment_group': 'd34218f3b4a3a4006d2153f17c76edff',  # ServiceNow 4th line
            'comments': "Initial description"
        })
        inserted = r.insert()
        self.assertTrue(inserted)

        t = Task(s)
        updated = t.resolve('Solution text', key=r.sys_id)
        self.assertTrue(updated)

        r2 = Record(s, 'incident')
        found = r2.get(r.sys_id)
        self.assertTrue(found)
        self.assertTrue(r2.incident_state, '6')
        self.assertTrue(r2.state, '6')
        self.assertTrue(r2.u_solution, 'Solution text')
        self.assertTrue(r2.u_close_code, 'Restored')
        self.assertTrue(r2.assigned_to, self.current_user)

        # third test: insert an incident, resolve it providing the number. No close code provided
        r = Record(s, 'incident', {  # s is a SnowRestSession object
            'short_description': self.short_description_prefix + ' test_resolve_3',
            'u_business_service': 'e85a3f3b0a0a8c0a006a2912f2f352d1',  # Service Element "ServiceNow"
            'u_functional_element': '579fb3d90a0a8c08017ac8a1137c8ee6',  # Functional Element "ServiceNow"
            'assignment_group': 'd34218f3b4a3a4006d2153f17c76edff',  # ServiceNow 4th line
            'comments': "Initial description"
        })
        inserted = r.insert()
        self.assertTrue(inserted)

        t = Task(s)
        updated = t.resolve('Solution text', key=('number', r.number))
        self.assertTrue(updated)

        r2 = Record(s, 'incident')
        found = r2.get(r.sys_id)
        self.assertTrue(found)
        self.assertTrue(r2.incident_state, '6')
        self.assertTrue(r2.state, '6')
        self.assertTrue(r2.u_solution, 'Solution text')
        self.assertTrue(r2.u_close_code, 'Restored')
        self.assertTrue(r2.assigned_to, self.current_user)

        # fourth test: insert an incident, get it, resolve it. Provide a non-default close code
        r = Record(s, 'incident', {  # s is a SnowRestSession object
            'short_description': self.short_description_prefix + ' test_resolve_4',
            'u_business_service': 'e85a3f3b0a0a8c0a006a2912f2f352d1',  # Service Element "ServiceNow"
            'u_functional_element': '579fb3d90a0a8c08017ac8a1137c8ee6',  # Functional Element "ServiceNow"
            'assignment_group': 'd34218f3b4a3a4006d2153f17c76edff',  # ServiceNow 4th line
            'comments': "Initial description"
        })
        inserted = r.insert()
        self.assertTrue(inserted)

        t = Task(s)
        found = t.get(r.sys_id)
        self.assertTrue(found)

        updated = t.resolve('Solution text', 'Not Reproducible')
        self.assertTrue(updated)

        r2 = Record(s, 'incident')
        found = r2.get(r.sys_id)
        self.assertTrue(found)
        self.assertTrue(r2.incident_state, '6')
        self.assertTrue(r2.state, '6')
        self.assertTrue(r2.u_solution, 'Solution text')
        self.assertTrue(r2.u_close_code, 'Not Reproducible')
        self.assertTrue(r2.assigned_to, self.current_user)

        # fifth test: insert a request, get it, resolve it. No close code provided
        r = Record(s, 'u_request_fulfillment', {  # s is a SnowRestSession object
            'short_description': self.short_description_prefix + ' test_resolve',
            'u_business_service': 'e85a3f3b0a0a8c0a006a2912f2f352d1',  # Service Element "ServiceNow"
            'u_functional_element': '579fb3d90a0a8c08017ac8a1137c8ee6',  # Functional Element "ServiceNow"
            'assignment_group': 'd34218f3b4a3a4006d2153f17c76edff',  # ServiceNow 4th line
            'comments': "Initial description"
        })
        inserted = r.insert()
        self.assertTrue(inserted)

        t = Task(s)
        found = t.get(r.sys_id)
        self.assertTrue(found)

        updated = t.resolve('Solution text')
        self.assertTrue(updated)

        r2 = Record(s, 'u_request_fulfillment')
        found = r2.get(r.sys_id)
        self.assertTrue(found)
        self.assertTrue(r2.u_current_task_state, '9')
        self.assertTrue(r2.state, '6')
        self.assertTrue(r2.u_solution, 'Solution text')
        self.assertTrue(r2.u_close_code, 'Fulfilled')
        self.assertTrue(r2.assigned_to, self.current_user)

        # sixth test: insert a request, resolve it by providing the number. Provide a non-default close code
        r = Record(s, 'u_request_fulfillment', {  # s is a SnowRestSession object
            'short_description': self.short_description_prefix + ' test_resolve_2',
            'u_business_service': 'e85a3f3b0a0a8c0a006a2912f2f352d1',  # Service Element "ServiceNow"
            'u_functional_element': '579fb3d90a0a8c08017ac8a1137c8ee6',  # Functional Element "ServiceNow"
            'assignment_group': 'd34218f3b4a3a4006d2153f17c76edff',  # ServiceNow 4th line
            'comments': "Initial description"
        })
        inserted = r.insert()
        self.assertTrue(inserted)

        t = Task(s)
        updated = t.resolve('Solution text', 'Not authorised', ('number', r.number))
        self.assertTrue(updated)

        r2 = Record(s, 'u_request_fulfillment')
        found = r2.get(r.sys_id)
        self.assertTrue(found)
        self.assertTrue(r2.u_current_task_state, '9')
        self.assertTrue(r2.state, '6')
        self.assertTrue(r2.u_solution, 'Solution text')
        self.assertTrue(r2.u_close_code, 'Not authorised')
        self.assertTrue(r2.assigned_to, self.current_user)

    def base_test_task_query(self, s):
        t = TaskQuery(s)

        # Query the incidents with FE=IT Service Management Support,
        # Visibility=CERN, Created in 2016, and already closed
        record_set = t.query(
            query_encoded="u_functional_element=ea56fb210a0a8c0a015a591ddbed3676^"
                          "u_visibility=cern^"
                          "active=false^"
                          "sys_class_name=incident^ORsys_class_name=u_request_fulfillment"
        )

        records_found = False
        for record in record_set:
            records_found = True
            self.assertTrue(bool(record.number))
            self.assertTrue(bool(record.short_description))
            self.assertTrue(record.sys_class_name == 'incident' or record.sys_class_name == 'u_request_fulfillment')
            self.assertTrue(type(record) is Task)
            self.assertFalse(hasattr(record, 'incident_state'))

        self.assertTrue(records_found)

        t2 = TaskQuery(s, 'incident')

        # Query the incidents with FE=IT Service Management Support,
        # Visibility=CERN, Created in 2016, and already closed
        record_set_2 = t2.query(
            query_encoded="u_functional_element=ea56fb210a0a8c0a015a591ddbed3676^u_visibility=cern^active=false^"
                          "sys_created_onDATEPART2016@javascript:gs.datePart('year','2016','EE')")

        records_found = False
        for record in record_set_2:
            records_found = True
            self.assertTrue(bool(record.number))
            self.assertTrue(bool(record.short_description))
            self.assertEquals(record.sys_class_name, 'incident')
            self.assertTrue(type(record) is Incident)
            self.assertTrue(hasattr(record, 'incident_state'))

        self.assertTrue(records_found)

        t3 = TaskQuery(s, 'task')

        # Query the incidents with FE=IT Service Management Support,
        # Visibility=CERN, Created in 2016, and already closed
        record_set_3 = t3.query(
            query_encoded="sys_class_name=incident^u_functional_element=ea56fb210a0a8c0a015a591ddbed3676"
                          "^u_visibility=cern^active=false^"
                          "sys_created_onDATEPART2016@javascript:gs.datePart('year','2016','EE')")

        records_found = False
        for record in record_set_3:
            records_found = True
            self.assertTrue(bool(record.number))
            self.assertTrue(bool(record.short_description))
            self.assertEquals(record.sys_class_name, 'incident')
            self.assertTrue(type(record) is Task)
            self.assertFalse(hasattr(record, 'incident_state'))

        self.assertTrue(records_found)
