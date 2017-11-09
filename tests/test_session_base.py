# coding: utf-8

import json

from tests.test_base import TestBase


class TestSessionBase(TestBase):

    def base_test_get(self, s):
        result = s.get('/api/now/v2/table/incident?sysparm_query=number=INC0426232')
        inc = json.loads(result.text)['result'][0]

        self.assertEquals(inc['number'], "INC0426232")
        self.assertEquals(inc['short_description'], "Test")

    def base_test_post(self, s):
        sd = self.short_description_prefix + ": test_insert_incident"
        fe = '579fb3d90a0a8c08017ac8a1137c8ee6'

        result = s.post('/api/now/v2/table/incident', data={
            'short_description': sd,
            'u_functional_element': fe,
            'incident_state': '2'
        })
        inc = json.loads(result.text)['result']

        print 'INC created: %s' % inc['number']

        self.assertEquals(inc['short_description'], sd)
        self.assertEquals(inc['u_functional_element']['value'], fe)
        self.assertEquals(inc['incident_state'], '2')

    def base_test_put(self, s):
        sd = self.short_description_prefix + ": test_update_incident"
        fe = '579fb3d90a0a8c08017ac8a1137c8ee6'

        result = s.post('/api/now/v2/table/incident', data={
            'short_description': sd,
            'u_functional_element': fe,
            'incident_state': '2',
            'watch_list': 'noreply@cern.ch'
        })
        inc = json.loads(result.text)['result']

        result2 = s.put('/api/now/v2/table/incident/' + inc['sys_id'], data={
            'watch_list': 'noreply2@cern.ch'
        })
        inc2 = json.loads(result2.text)['result']

        result3 = s.get('/api/now/v2/table/incident/' + inc['sys_id'])
        inc3 = json.loads(result3.text)['result']

        print 'INC created: %s' % inc['number']

        self.assertEquals(inc2['watch_list'], 'noreply2@cern.ch')
        self.assertEquals(inc3['watch_list'], 'noreply2@cern.ch')

    def base_test_session_persistance(self, s):
        result1 = s.get('/api/now/v2/table/incident?sysparm_query=number=INC0426232')
        inc1 = json.loads(result1.text)['result'][0]
        session_id1 = TestSessionBase.get_cookie_by_name(s.session.cookies, 'JSESSIONID')

        result2 = s.get('/api/now/v2/table/incident?sysparm_query=number=INC0426232')
        inc2 = json.loads(result2.text)['result'][0]
        session_id2 = TestSessionBase.get_cookie_by_name(s.session.cookies, 'JSESSIONID')

        self.assertEquals(inc1['number'], inc2['number'])
        self.assertEquals(inc1['short_description'], inc2['short_description'])
        self.assertEquals(session_id1, session_id2)
