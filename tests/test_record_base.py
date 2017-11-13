# coding: utf-8

from cern_snow_client.record import Record
from tests.test_base import TestBase


class TestRecordBase(TestBase):

    def base_test_get_record(self, s):
        r = Record(s, 'incident')  # s is a SnowRestSession object
        found = r.get('c1c535ba85f45540adf94de5b835cd43')

        self.assertTrue(found)

        self.assertEquals(str(r.number), 'INC0426232')
        self.assertEquals(str(r.sys_id), 'c1c535ba85f45540adf94de5b835cd43')
        self.assertEquals(str(r.sys_class_name), 'incident')
        
        self.assertEquals(str(r.short_description), 'Test')
        self.assertEquals(r.short_description.get_value(), 'Test')
        self.assertEquals(r.short_description.get_display_value(), 'Test')
        self.assertFalse(r.short_description.is_reference())

        self.assertEquals(str(r.u_functional_element), 'ea56fb210a0a8c0a015a591ddbed3676')
        self.assertEquals(r.u_functional_element.get_value(), 'ea56fb210a0a8c0a015a591ddbed3676')
        self.assertEquals(r.u_functional_element.get_display_value(), 'IT Service Management Support')
        self.assertTrue(r.u_functional_element.is_reference())
        self.assertEquals(r.u_functional_element.get_referenced_table(), 'u_cmdb_ci_functional_services')

        self.assertEquals(str(r.incident_state), '7')
        self.assertEquals(r.incident_state.get_value(), '7')
        self.assertEquals(r.incident_state.get_display_value(), 'Closed')
        self.assertFalse(r.incident_state.is_reference())

    def base_test_insert_record(self, s):
        # TODO: implement this test
        r = Record(s, 'incident', {'short_description' : "New incident", 'u_business_service' : 'e85a3f3b0a0a8c0a006a2912f2f352d1', 'u_functional_element' : '579fb3d90a0a8c08017ac8a1137c8ee6','comments' : "Initial description", 'incident_state'})
        inserted = r.insert()
        
        r2 = Record(s, 'incident')
        found = r2.get(r.sys_id)

        self.assertTrue(inserted)
        self.assertTrue(found)
        
        
                
    
    def base_test_update_record(self, s):
        # TODO: implement this test
        pass
