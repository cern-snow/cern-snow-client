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

import json

from tests.test_base import TestBase


class TestSessionBase(TestBase):

    def base_test_get(self, s):
        result = s.get('/api/now/v2/table/incident?sysparm_query=number=INC0426232')
        inc = json.loads(result.text)['result'][0]

        self.assertEquals(result.status_code, 200)
        self.assertEquals(inc['number'], "INC0426232")
        self.assertEquals(inc['short_description'], "Test")

    def base_test_post(self, s):
        sd = self.short_description_prefix + ": test_post"
        fe = '579fb3d90a0a8c08017ac8a1137c8ee6'
        data = json.dumps({
            'short_description': sd,
            'u_functional_element': fe,
            'comments': 'Initial description'
        })

        result = s.post('/api/now/v2/table/incident', data=data)
        self.assertEquals(result.status_code, 201)
        inc = json.loads(result.text)['result']

        self.assertEquals(inc['short_description'], sd)
        self.assertEquals(inc['u_functional_element']['value'], fe)
        self.assertEquals(inc['incident_state'], '2')

    def base_test_put(self, s):
        sd = self.short_description_prefix + ": test_put"
        fe = '579fb3d90a0a8c08017ac8a1137c8ee6'
        data = json.dumps({
            'short_description': sd,
            'u_functional_element': fe,
            'watch_list': 'noreply@cern.ch'
        })

        result = s.post('/api/now/v2/table/incident', data=data)
        self.assertEquals(result.status_code, 201)
        inc = json.loads(result.text)['result']

        data = json.dumps({
            'watch_list': 'noreply2@cern.ch'
        })
        result2 = s.put('/api/now/v2/table/incident/' + inc['sys_id'], data=data)
        self.assertEquals(result2.status_code, 200)
        inc2 = json.loads(result2.text)['result']

        result3 = s.get('/api/now/v2/table/incident/' + inc['sys_id'])
        self.assertEquals(result3.status_code, 200)
        inc3 = json.loads(result3.text)['result']

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
