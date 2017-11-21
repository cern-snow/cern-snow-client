# coding: utf-8

from cern_snow_client.record import Record
from cern_snow_client.record import RecordQuery
from cern_snow_client.task import Task
from cern_snow_client.incident import Incident
from tests.test_base import TestBase


class TestTaskBase(TestBase):

    def base_test_add_comment(self, s):
        r = Record(s, 'incident', {  # s is a SnowRestSession object
            'short_description': self.short_description_prefix + ' test_add_comment',
            'u_business_service': 'e85a3f3b0a0a8c0a006a2912f2f352d1',  # Service Element "ServiceNow"
            'u_functional_element': '579fb3d90a0a8c08017ac8a1137c8ee6',  # Functional Element "ServiceNow"
            'assignment_group': 'd34218f3b4a3a4006d2153f17c76edff',  # ServiceNow 4th line
            'comments': "Initial description",
            'incident_state': '2'  # initial state : Assigned
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
            'comments': "Initial description",
            'incident_state': '2'  # initial state : Assigned
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
        pass

    def base_test_resolve(self, s):
        pass

    def base_test_task_query(self, s):
        pass
