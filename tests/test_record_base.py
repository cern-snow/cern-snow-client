# coding: utf-8

from cern_snow_client.record import Record
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

        self.assertEquals(r.incident_status, '7')
        self.assertEquals(r.incident_status.get_value(), '7')
        self.assertEquals(r.incident_status.get_display_value(), 'Closed')
        self.assertFalse(r.incident_status.is_reference())

    def base_test_insert_record(self, s):
        # TODO: implement this test
        pass

    def base_test_update_record(self, s):
        # TODO: implement this test
        pass
