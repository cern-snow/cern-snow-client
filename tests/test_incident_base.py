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

from cern_snow_client.incident import Incident
from cern_snow_client.incident import IncidentQuery
from tests.test_base import TestBase


class TestIncidentBase(TestBase):

    def base_test_incident_get(self, s):
        i = Incident(s)
        found = i.get('c1c535ba85f45540adf94de5b835cd43')
        self.assertTrue(found)
        self.assertEquals(i.sys_id, 'c1c535ba85f45540adf94de5b835cd43')
        self.assertEquals(i.number, 'INC0426232')
        self.assertEquals(i.short_description, 'Test')
        self.assertEquals(i.get_table_name(), 'incident')
        self.assertEquals(i.sys_class_name, 'incident')
        self.assertEquals(i.incident_state, '7')

        i = Incident(s)
        found = i.get(('number', 'INC0426232'))
        self.assertTrue(found)
        self.assertEquals(i.sys_id, 'c1c535ba85f45540adf94de5b835cd43')
        self.assertEquals(i.number, 'INC0426232')
        self.assertEquals(i.short_description, 'Test')
        self.assertEquals(i.get_table_name(), 'incident')
        self.assertEquals(i.sys_class_name, 'incident')
        self.assertEquals(i.incident_state, '7')

        i = Incident(s)
        found = i.get(('number', 'RQF0746626'))
        self.assertFalse(found)

    def base_test_incident_insert(self, s):
        # incident test with values in constructor
        i_original = Incident(s, {
            'short_description': self.short_description_prefix + ' test_insert_incident_1',
            'u_business_service': 'e85a3f3b0a0a8c0a006a2912f2f352d1',  # Service Element "ServiceNow"
            'u_functional_element': '579fb3d90a0a8c08017ac8a1137c8ee6',  # Functional Element "ServiceNow"
            'assignment_group': 'd34218f3b4a3a4006d2153f17c76edff',  # ServiceNow 4th line
            'comments': "Initial description"
        })
        self.assertTrue(i_original.get_can_insert())
        inserted = i_original.insert()
        self.assertTrue(inserted)
        self.assertTrue(i_original.sys_id is not None)
        self.assertEquals(i_original.get_table_name(), 'incident')
        self.assertEquals(i_original.sys_class_name, 'incident')
        self.assertEquals(i_original.short_description, self.short_description_prefix + ' test_insert_incident_1')
        self.assertEquals(i_original.u_business_service, 'e85a3f3b0a0a8c0a006a2912f2f352d1')
        self.assertEquals(i_original.u_functional_element, '579fb3d90a0a8c08017ac8a1137c8ee6')
        self.assertEquals(i_original.assignment_group, 'd34218f3b4a3a4006d2153f17c76edff')
        self.assertEquals(i_original.description, 'Initial description')
        self.assertEquals(i_original.incident_state, '2')

        i = Incident(s)
        found = i.get(i_original.sys_id)
        self.assertTrue(found)

        self.assertEquals(i.sys_class_name, 'incident')
        self.assertEquals(i.short_description, self.short_description_prefix + ' test_insert_incident_1')
        self.assertEquals(i.u_business_service, 'e85a3f3b0a0a8c0a006a2912f2f352d1')
        self.assertEquals(i.u_functional_element, '579fb3d90a0a8c08017ac8a1137c8ee6')
        self.assertEquals(i.assignment_group, 'd34218f3b4a3a4006d2153f17c76edff')
        self.assertEquals(i.description, 'Initial description')
        self.assertEquals(i.incident_state, '2')

        # incident test, setting values after constructor
        i_original = Incident(s)
        i_original.short_description = self.short_description_prefix + ' test_insert_incident_2'
        i_original.u_business_service = 'e85a3f3b0a0a8c0a006a2912f2f352d1'  # Service Element "ServiceNow"
        i_original.u_functional_element = '579fb3d90a0a8c08017ac8a1137c8ee6'  # Functional Element "ServiceNow"
        i_original.assignment_group = 'd34218f3b4a3a4006d2153f17c76edff'  # ServiceNow 4th line
        i_original.comments = "Initial description"
        inserted = i_original.insert()
        self.assertTrue(i_original.get_can_insert())

        self.assertTrue(inserted)
        self.assertTrue(i_original.sys_id is not None)
        self.assertEquals(i_original.get_table_name(), 'incident')
        self.assertEquals(i_original.sys_class_name, 'incident')
        self.assertEquals(i_original.short_description, self.short_description_prefix + ' test_insert_incident_2')
        self.assertEquals(i_original.u_business_service, 'e85a3f3b0a0a8c0a006a2912f2f352d1')
        self.assertEquals(i_original.u_functional_element, '579fb3d90a0a8c08017ac8a1137c8ee6')
        self.assertEquals(i_original.assignment_group, 'd34218f3b4a3a4006d2153f17c76edff')
        self.assertEquals(i_original.description, 'Initial description')
        self.assertEquals(i_original.incident_state, '2')

        i = Incident(s)
        found = i.get(i_original.sys_id)
        self.assertTrue(found)

        self.assertEquals(i.sys_class_name, 'incident')
        self.assertEquals(i.number, i.number)
        self.assertEquals(i.short_description, self.short_description_prefix + ' test_insert_incident_2')
        self.assertEquals(i.u_business_service, 'e85a3f3b0a0a8c0a006a2912f2f352d1')
        self.assertEquals(i.u_functional_element, '579fb3d90a0a8c08017ac8a1137c8ee6')
        self.assertEquals(i.assignment_group, 'd34218f3b4a3a4006d2153f17c76edff')
        self.assertEquals(i.description, 'Initial description')
        self.assertEquals(i.incident_state, '2')

    def base_test_incident_update(self, s):
        # insert an incident for testing
        i_original = Incident(s, {
            'short_description': self.short_description_prefix + ' test_update_incident_1',
            'u_business_service': 'e85a3f3b0a0a8c0a006a2912f2f352d1',  # Service Element "ServiceNow"
            'u_functional_element': '579fb3d90a0a8c08017ac8a1137c8ee6',  # Functional Element "ServiceNow"
            'assignment_group': 'd34218f3b4a3a4006d2153f17c76edff',  # ServiceNow 4th line
            'comments': "Initial description"
        })
        inserted = i_original.insert()
        self.assertTrue(inserted)

        # get the incident and the update it
        i = Incident(s)
        found = i.get(i_original.sys_id)
        self.assertTrue(found)
        i.watch_list = 'test_watch_list_value@cern.ch'
        updated = i.update()
        self.assertTrue(updated)
        self.assertEquals(i.watch_list, 'test_watch_list_value@cern.ch')

        i = Incident(s)
        found = i.get(i_original.sys_id)
        self.assertTrue(found)
        self.assertEquals(i.watch_list, 'test_watch_list_value@cern.ch')

        # update the incident by sys_id without getting it
        i = Incident(s)
        i.watch_list = 'test_watch_list_value_2@cern.ch'
        updated = i.update(i_original.sys_id)
        self.assertTrue(updated)
        self.assertEquals(i.watch_list, 'test_watch_list_value_2@cern.ch')

        i = Incident(s)
        found = i.get(i_original.sys_id)
        self.assertTrue(found)
        self.assertEquals(i.watch_list, 'test_watch_list_value_2@cern.ch')

        # update the incident by number without getting it
        i = Incident(s)
        i.watch_list = 'test_watch_list_value_3@cern.ch'
        updated = i.update(('number', i_original.number))
        self.assertTrue(updated)
        self.assertEquals(i.watch_list, 'test_watch_list_value_3@cern.ch')

        i = Incident(s)
        found = i.get(i_original.sys_id)
        self.assertTrue(found)
        self.assertEquals(i.watch_list, 'test_watch_list_value_3@cern.ch')

        # update the incident_state after getting it
        i = Incident(s)
        found = i.get(i_original.sys_id)
        self.assertTrue(found)
        i.incident_state = '3'
        updated = i.update()
        self.assertTrue(updated)
        self.assertEquals(i.incident_state, '3')

        i = Incident(s)
        found = i.get(i_original.sys_id)
        self.assertTrue(found)
        self.assertEquals(i.incident_state, '3')

        # update the incident_state directly by sys_id
        i = Incident(s)
        i.incident_state = '4'
        updated = i.update(i_original.sys_id)
        self.assertTrue(updated)
        self.assertEquals(i.incident_state, '4')

        i = Incident(s)
        found = i.get(i_original.sys_id)
        self.assertTrue(found)
        self.assertEquals(i.incident_state, '4')

        # update the incident_state directly by number
        i = Incident(s)
        i.incident_state = '3'
        updated = i.update(('number', i_original.number))
        self.assertTrue(updated)
        self.assertEquals(i.incident_state, '3')

        i = Incident(s)
        found = i.get(i_original.sys_id)
        self.assertTrue(found)
        self.assertEquals(i.incident_state, '3')

    def base_test_incident_add_comment(self, s):
        i_original = Incident(s, {  # s is a SnowRestSession object
            'short_description': self.short_description_prefix + ' test_incident_add_comment',
            'u_business_service': 'e85a3f3b0a0a8c0a006a2912f2f352d1',  # Service Element "ServiceNow"
            'u_functional_element': '579fb3d90a0a8c08017ac8a1137c8ee6',  # Functional Element "ServiceNow"
            'assignment_group': 'd34218f3b4a3a4006d2153f17c76edff',  # ServiceNow 4th line
            'comments': "Initial description"
        })
        inserted = i_original.insert()
        self.assertTrue(inserted)

        i = Incident(s)
        found = i.get(i_original.sys_id)
        self.assertTrue(found)

        updated = i.add_comment('New comment')
        self.assertTrue(updated)

        i = Incident(s)
        updated = i.add_comment('New comment 2', i_original.sys_id)
        self.assertTrue(updated)

        i = Incident(s)
        updated = i.add_comment('New comment 3', ('number', i_original.number))
        self.assertTrue(updated)

    def base_test_incident_add_work_note(self, s):
        i_original = Incident(s, {  # s is a SnowRestSession object
            'short_description': self.short_description_prefix + ' test_incident_add_work_note',
            'u_business_service': 'e85a3f3b0a0a8c0a006a2912f2f352d1',  # Service Element "ServiceNow"
            'u_functional_element': '579fb3d90a0a8c08017ac8a1137c8ee6',  # Functional Element "ServiceNow"
            'assignment_group': 'd34218f3b4a3a4006d2153f17c76edff',  # ServiceNow 4th line
            'comments': "Initial description"
        })
        inserted = i_original.insert()
        self.assertTrue(inserted)

        i = Incident(s)
        found = i.get(i_original.sys_id)
        self.assertTrue(found)

        updated = i.add_work_note('New work note')
        self.assertTrue(updated)

        i = Incident(s)
        updated = i.add_work_note('New work note 2', i_original.sys_id)
        self.assertTrue(updated)

        i = Incident(s)
        updated = i.add_work_note('New work note 3', ('number', i_original.number))
        self.assertTrue(updated)

    def base_test_incident_take_in_progress(self, s):
        # first test: insert an incident, get it, take it in progress
        r = Incident(s, {  # s is a SnowRestSession object
            'short_description': self.short_description_prefix + ' test_incident_take_in_progress',
            'u_business_service': 'e85a3f3b0a0a8c0a006a2912f2f352d1',  # Service Element "ServiceNow"
            'u_functional_element': '579fb3d90a0a8c08017ac8a1137c8ee6',  # Functional Element "ServiceNow"
            'assignment_group': 'd34218f3b4a3a4006d2153f17c76edff',  # ServiceNow 4th line
            'comments': "Initial description"
        })
        inserted = r.insert()
        self.assertTrue(inserted)

        t = Incident(s)
        found = t.get(r.sys_id)
        self.assertTrue(found)

        updated = t.take_in_progress()
        self.assertTrue(updated)

        r2 = Incident(s)
        found = r2.get(r.sys_id)
        self.assertTrue(found)
        self.assertTrue(r2.incident_state, '3')
        self.assertTrue(r2.state, '2')
        self.assertTrue(r2.assigned_to, self.current_user)

        # second test: insert an incident, take it in progress by providing the sys_id
        r = Incident(s, {  # s is a SnowRestSession object
            'short_description': self.short_description_prefix + ' test_incident_take_in_progress_2',
            'u_business_service': 'e85a3f3b0a0a8c0a006a2912f2f352d1',  # Service Element "ServiceNow"
            'u_functional_element': '579fb3d90a0a8c08017ac8a1137c8ee6',  # Functional Element "ServiceNow"
            'assignment_group': 'd34218f3b4a3a4006d2153f17c76edff',  # ServiceNow 4th line
            'comments': "Initial description"
        })
        inserted = r.insert()
        self.assertTrue(inserted)

        t = Incident(s)
        updated = t.take_in_progress(key=r.sys_id)
        self.assertTrue(updated)

        r2 = Incident(s)
        found = r2.get(r.sys_id)
        self.assertTrue(found)
        self.assertTrue(r2.incident_state, '3')
        self.assertTrue(r2.state, '2')
        self.assertTrue(r2.assigned_to, self.current_user)

        # third test: insert an incident, take it in progress by providing the number
        r = Incident(s, {  # s is a SnowRestSession object
            'short_description': self.short_description_prefix + ' test_incident_take_in_progress_3',
            'u_business_service': 'e85a3f3b0a0a8c0a006a2912f2f352d1',  # Service Element "ServiceNow"
            'u_functional_element': '579fb3d90a0a8c08017ac8a1137c8ee6',  # Functional Element "ServiceNow"
            'assignment_group': 'd34218f3b4a3a4006d2153f17c76edff',  # ServiceNow 4th line
            'comments': "Initial description"
        })
        inserted = r.insert()
        self.assertTrue(inserted)

        t = Incident(s)
        updated = t.take_in_progress(key=('number', r.number))
        self.assertTrue(updated)

        r2 = Incident(s)
        found = r2.get(r.sys_id)
        self.assertTrue(found)
        self.assertTrue(r2.incident_state, '3')
        self.assertTrue(r2.state, '2')
        self.assertTrue(r2.assigned_to, self.current_user)

    def base_test_incident_resolve(self, s):
        # first test: insert an incident, get it, resolve it. No close code provided
        i_original = Incident(s, {  # s is a SnowRestSession object
            'short_description': self.short_description_prefix + ' test_incident_resolve',
            'u_business_service': 'e85a3f3b0a0a8c0a006a2912f2f352d1',  # Service Element "ServiceNow"
            'u_functional_element': '579fb3d90a0a8c08017ac8a1137c8ee6',  # Functional Element "ServiceNow"
            'assignment_group': 'd34218f3b4a3a4006d2153f17c76edff',  # ServiceNow 4th line
            'comments': "Initial description"
        })
        inserted = i_original.insert()
        self.assertTrue(inserted)

        i = Incident(s)
        found = i.get(i_original.sys_id)
        self.assertTrue(found)

        updated = i.resolve('Solution text')
        self.assertTrue(updated)

        i = Incident(s)
        found = i.get(i_original.sys_id)
        self.assertTrue(found)
        self.assertTrue(i.incident_state, '6')
        self.assertTrue(i.state, '6')
        self.assertTrue(i.u_solution, 'Solution text')
        self.assertTrue(i.u_close_code, 'Restored')
        self.assertTrue(i.assigned_to, self.current_user)

        # second test: insert an incident, resolve it providing the sys_id. No close code provided
        i_original = Incident(s, {  # s is a SnowRestSession object
            'short_description': self.short_description_prefix + ' test_incident_resolve_2',
            'u_business_service': 'e85a3f3b0a0a8c0a006a2912f2f352d1',  # Service Element "ServiceNow"
            'u_functional_element': '579fb3d90a0a8c08017ac8a1137c8ee6',  # Functional Element "ServiceNow"
            'assignment_group': 'd34218f3b4a3a4006d2153f17c76edff',  # ServiceNow 4th line
            'comments': "Initial description"
        })
        inserted = i_original.insert()
        self.assertTrue(inserted)

        i = Incident(s)
        updated = i.resolve('Solution text', key=i_original.sys_id)
        self.assertTrue(updated)

        i = Incident(s)
        found = i.get(i_original.sys_id)
        self.assertTrue(found)
        self.assertTrue(i.incident_state, '6')
        self.assertTrue(i.state, '6')
        self.assertTrue(i.u_solution, 'Solution text')
        self.assertTrue(i.u_close_code, 'Restored')
        self.assertTrue(i.assigned_to, self.current_user)

        # third test: insert an incident, resolve it providing the number. No close code provided
        i_original = Incident(s, {  # s is a SnowRestSession object
            'short_description': self.short_description_prefix + ' test_incident_resolve_3',
            'u_business_service': 'e85a3f3b0a0a8c0a006a2912f2f352d1',  # Service Element "ServiceNow"
            'u_functional_element': '579fb3d90a0a8c08017ac8a1137c8ee6',  # Functional Element "ServiceNow"
            'assignment_group': 'd34218f3b4a3a4006d2153f17c76edff',  # ServiceNow 4th line
            'comments': "Initial description"
        })
        inserted = i_original.insert()
        self.assertTrue(inserted)

        i = Incident(s)
        updated = i.resolve('Solution text', key=('number', i_original.number))
        self.assertTrue(updated)

        i = Incident(s)
        found = i.get(i_original.sys_id)
        self.assertTrue(found)
        self.assertTrue(i.incident_state, '6')
        self.assertTrue(i.state, '6')
        self.assertTrue(i.u_solution, 'Solution text')
        self.assertTrue(i.u_close_code, 'Restored')
        self.assertTrue(i.assigned_to, self.current_user)

        # fourth test: insert an incident, get it, resolve ii. Provide a non-default close code
        i_original = Incident(s, {  # s is a SnowRestSession object
            'short_description': self.short_description_prefix + ' test_incident_resolve_4',
            'u_business_service': 'e85a3f3b0a0a8c0a006a2912f2f352d1',  # Service Element "ServiceNow"
            'u_functional_element': '579fb3d90a0a8c08017ac8a1137c8ee6',  # Functional Element "ServiceNow"
            'assignment_group': 'd34218f3b4a3a4006d2153f17c76edff',  # ServiceNow 4th line
            'comments': "Initial description"
        })
        inserted = i_original.insert()
        self.assertTrue(inserted)

        i = Incident(s)
        found = i.get(i_original.sys_id)
        self.assertTrue(found)

        updated = i.resolve('Solution text', 'Not Reproducible')
        self.assertTrue(updated)

        i = Incident(s)
        found = i.get(i_original.sys_id)
        self.assertTrue(found)
        self.assertTrue(i.incident_state, '6')
        self.assertTrue(i.state, '6')
        self.assertTrue(i.u_solution, 'Solution text')
        self.assertTrue(i.u_close_code, 'Not Reproducible')
        self.assertTrue(i.assigned_to, self.current_user)

    def base_test_incident_query(self, s):
        i = IncidentQuery(s)

        # Query the incidents with FE=IT Service Management Support,
        # Visibility=CERN, Created in 2016, and already closed
        record_set = i.query(query_filter={
            'u_functional_element': 'ea56fb210a0a8c0a015a591ddbed3676',
            'u_visibility': 'cern',
            'active': 'false'
        })

        records_found = False
        for record in record_set:
            records_found = True
            self.assertTrue(bool(record.number))
            self.assertTrue(bool(record.short_description))
            self.assertEquals(record.sys_class_name, 'incident')
            self.assertTrue(type(record) is Incident)
            self.assertTrue(hasattr(record, 'incident_state'))

        self.assertTrue(records_found)

        i = IncidentQuery(s)

        # Query the incidents with FE=IT Service Management Support,
        # Visibility=CERN, Created in 2016, and already closed
        record_set = i.query(
            query_encoded="u_functional_element=ea56fb210a0a8c0a015a591ddbed3676^u_visibility=cern^active=false^"
                          "sys_created_onDATEPART2016@javascript:gs.datePart('year','2016','EE')")

        records_found = False
        for record in record_set:
            records_found = True
            self.assertTrue(bool(record.number))
            self.assertTrue(bool(record.short_description))
            self.assertEquals(record.sys_class_name, 'incident')
            self.assertTrue(type(record) is Incident)
            self.assertTrue(hasattr(record, 'incident_state'))

        self.assertTrue(records_found)
