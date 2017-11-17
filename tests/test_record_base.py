# coding: utf-8

from cern_snow_client.record import Record
from cern_snow_client.record import RecordQuery
from cern_snow_client.task import Task
from cern_snow_client.incident import Incident
from tests.test_base import TestBase


class TestRecordBase(TestBase):

    def base_test_get_record(self, s):
        r = Record(s, 'incident')  # s is a SnowRestSession object
        found = r.get('c1c535ba85f45540adf94de5b835cd43')

        self.assertTrue(found)

        self.assertEquals(r.number, 'INC0426232')
        self.assertEquals(r.sys_id, 'c1c535ba85f45540adf94de5b835cd43')
        self.assertEquals(r.sys_class_name, 'incident')

        self.assertEquals(r.short_description, 'Test')
        self.assertEquals(r.short_description.get_value(), 'Test')
        self.assertEquals(r.short_description.get_display_value(), 'Test')
        self.assertFalse(r.short_description.is_reference())

        self.assertEquals(r.u_functional_element, 'ea56fb210a0a8c0a015a591ddbed3676')
        self.assertEquals(r.u_functional_element.get_value(), 'ea56fb210a0a8c0a015a591ddbed3676')
        self.assertEquals(r.u_functional_element.get_display_value(), 'IT Service Management Support')
        self.assertTrue(r.u_functional_element.is_reference())
        self.assertEquals(r.u_functional_element.get_referenced_table(), 'u_cmdb_ci_functional_services')

        self.assertEquals(r.incident_state, '7')
        self.assertEquals(r.incident_state.get_value(), '7')
        self.assertEquals(r.incident_state.get_display_value(), 'Closed')
        self.assertFalse(r.incident_state.is_reference())

    def base_test_insert_record(self, s):
        r = Record(s, 'incident', {  # s is a SnowRestSession object
            'short_description': self.short_description_prefix + ' test_insert_record',
            'u_business_service': 'e85a3f3b0a0a8c0a006a2912f2f352d1',  # Service Element "ServiceNow"
            'u_functional_element': '579fb3d90a0a8c08017ac8a1137c8ee6',  # Functional Element "ServiceNow"
            'comments': "Initial description",
            'incident_state': '2'  # initial state : Assigned
        })
        inserted = r.insert()
        
        r2 = Record(s, 'incident')
        found = r2.get(r.sys_id)

        self.assertTrue(inserted)
        self.assertTrue(found)

        self.assertEquals(r.number, r2.number)
        self.assertEquals(r.short_description,r2.short_description)
        self.assertEquals(r.u_business_service, r2.u_business_service)
        self.assertEquals(r.u_functional_element, r2.u_functional_element)
        self.assertEquals(r.comments, r2.comments)
    
    def base_test_update_record(self, s):
        r = Record(s, 'incident', {  # s is a SnowRestSession object
            'short_description': self.short_description_prefix + ' test_update_record',
            'u_business_service': 'e85a3f3b0a0a8c0a006a2912f2f352d1',  # Service Element "ServiceNow"
            'u_functional_element': '579fb3d90a0a8c08017ac8a1137c8ee6',  # Functional Element "ServiceNow"
            'comments': "Initial description",
            'incident_state': '2'  # initial state : Assigned
        })
        inserted = r.insert()
        self.assertTrue(inserted)

        r2 = Record(s, 'incident')
        found = r2.get(('number', r.number))
        self.assertTrue(found)
        self.assertEquals(r.number, r2.number)
        self.assertEquals(r2.short_description, self.short_description_prefix + ' test_update_record')

        r2.watch_list = 'test_watch_list_value@cern.ch'
        updated = r2.update()
        self.assertTrue(updated)

        r3 = Record(s, 'incident')
        found = r3.get(('number', r.number))
        self.assertTrue(found)
        self.assertEquals(r3.watch_list, 'test_watch_list_value@cern.ch')

        r4 = Record(s, 'incident')
        r4.watch_list = 'test_watch_list_value_2@cern.ch'
        updated = r4.update(('number', r.number))
        self.assertTrue(updated)

        r5 = Record(s, 'incident')
        found = r5.get(('number', r.number))
        self.assertTrue(found)
        self.assertEquals(r5.watch_list, 'test_watch_list_value_2@cern.ch')

    def base_test_get_query(self, s):
        r = RecordQuery(s, 'incident')

        # Query the incidents with FE=IT Service Management Support,
        # Visibility=CERN, Created in 2016, and already closed
        record_set = r.query(
            query_encoded="u_functional_element=ea56fb210a0a8c0a015a591ddbed3676^u_visibility=cern^"
                          "sys_created_onDATEPART2016@javascript:gs.datePart('year','2016','EE')^active=false")

        records_found = False
        for record in record_set:
            records_found = True
            self.assertIsNotNone(record.number)
            self.assertIsNotNone(record.short_description)
            self.assertEquals(record.sys_class_name, 'incident')
            self.assertIs(type(record), Incident)

        self.assertTrue(records_found)

        r2 = RecordQuery(s, 'task')

        # Query the incidents with FE=IT Service Management Support,
        # Visibility=CERN, Created in 2016, and already closed
        record_set_2 = r2.query(
            query_encoded="sys_class_name=incident^u_functional_element=ea56fb210a0a8c0a015a591ddbed3676"
                          "^u_visibility=cern^active=false^"
                          "sys_created_onDATEPART2016@javascript:gs.datePart('year','2016','EE')")

        records_found = False
        for record in record_set_2:
            records_found = True
            self.assertIsNotNone(record.number)
            self.assertIsNotNone(record.short_description)
            self.assertEquals(record.sys_class_name, 'incident')
            self.assertIs(type(record), Task)

        self.assertTrue(records_found)
