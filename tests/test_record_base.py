# coding: utf-8

from cern_snow_client.record import Record
from cern_snow_client.record import RecordQuery
from cern_snow_client.record import RecordSet
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
        r = Record(s, 'incident', {"u_business_service": "e85a376e0a0a8c0a004ca384c6043fe1",
                                   "u_functional_element": "ea56f72a0a0a8c0a010f2fddfd8e0a68",
                                   "assignment_group": "ea56f7310a0a8c0a001b376fe5aa9cc6",
                                   "short_description": "Incident for presentation by JAMES", "comments": "HELLO"})
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
        pass
        #r = Record(s, 'incident', {"u_business_service": "e85a376e0a0a8c0a004ca384c6043fe1","u_functional_element": "ea56f72a0a0a8c0a010f2fddfd8e0a68","assignment_group": "ea56f7310a0a8c0a001b376fe5aa9cc6","short_description": "Incident for presentation by JAMES","comments": "HELLO", "incident_state" : "2"})
        #inserted = r.insert()
        #self.assertTrue(inserted)

        #r = Record(s, 'incident')
        #incident = r.get(('number', 'INC1490808'))
        #if r.watch_list:
        #    r.watch_list = r.watch_list + ','
        #    r.watch_list = r.watch_list + 'david.martin.clavo@cern.ch'
        #if r.work_note:
        #    r.work_note = 'incident worknote'
        #r.update()
        #print r.watch_list
        #print r.number

        #r2 = Record(s, 'incident')
        #updated = r2.get(r.sys_id)
        #self.assertTrue(updated)
        #print r2.watch_list
        #print 'updated is true'

    def base_test_get_query(self, s):
        r = RecordQuery(s, 'incident')
        query = r.query(query_encoded='sys_created_onONToday^short_descriptionISNOTEMPTY')
        if query._result_array:
            for incident in query._result_array:
                print incident['number']
        else:
            print 'Problem in the query, the result is empty'