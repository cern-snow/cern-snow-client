import json
import yaml

from cern_snow_client.session import SnowRestSession


class TestBase(object):

    short_description_prefix = "snow client unit test"

    @staticmethod
    def make_session(config_file_path):
        s = SnowRestSession()
        s.load_config_file(config_file_path)
        return s

    @staticmethod
    def get_password(password_name):
        passwords_file_path = 'tests/config_files/passwords.yaml'

        with open(passwords_file_path) as f:
            passwords = yaml.safe_load(f)
            return passwords[password_name]

    @staticmethod
    def get_cookie_by_name(cookie_jar, cookie_name):
        for cookie in cookie_jar:
            if cookie.name == cookie_name:
                return cookie.value
        return None

    def test_get_incident(self, s):
        result = s.get_incident(number='INC0426232')
        inc = json.loads(result.text)['result'][0]

        self.assertEquals(inc['number'], "INC0426232")
        self.assertEquals(inc['short_description'], "Test")

    def test_insert_incident(self, s):
        sd = self.short_description_prefix + ": test_insert_incident"
        fe = '579fb3d90a0a8c08017ac8a1137c8ee6'

        result = s.insert_incident(data={
            'short_description': sd,
            'u_functional_element': fe,
            'incident_state': '2'
        })
        inc = json.loads(result.text)['result']

        print 'INC created: %s' % inc['number']

        self.assertEquals(inc['short_description'], sd)
        self.assertEquals(inc['u_functional_element']['value'], fe)
        self.assertEquals(inc['incident_state'], '2')

    def test_update_incident(self, s):
        sd = self.short_description_prefix + ": test_update_incident"
        fe = '579fb3d90a0a8c08017ac8a1137c8ee6'

        result = s.insert_incident(data={
            'short_description': sd,
            'u_functional_element': fe,
            'incident_state': '2',
            'watch_list': 'noreply@cern.ch'
        })
        inc = json.loads(result.text)['result']

        result2 = s.update_incident(sys_id=inc['sys_id'], data={
            'watch_list': 'noreply2@cern.ch'
        })
        inc2 = json.loads(result2.text)['result']

        result3 = s.get_incident(sys_id=inc['sys_id'])
        inc3 = json.loads(result3.text)['result']

        result4 = s.update_incident(number=inc['number'], data={
            'watch_list': 'noreply3@cern.ch'
        })
        inc4 = json.loads(result4.text)['result']

        result5 = s.get_incident(sys_id=inc['sys_id'])
        inc5 = json.loads(result5.text)['result']

        print 'INC created: %s' % inc['number']

        self.assertEquals(inc2['watch_list'], 'noreply2@cern.ch')
        self.assertEquals(inc3['watch_list'], 'noreply2@cern.ch')
        self.assertEquals(inc4['watch_list'], 'noreply3@cern.ch')
        self.assertEquals(inc5['watch_list'], 'noreply3@cern.ch')

    def test_session_persistance(self, s):
        result1 = s.get_incident(number='INC0426232')
        inc1 = json.loads(result1.text)['result'][0]
        session_id1 = TestBase.get_cookie_by_name(s.session.cookies, 'JSESSIONID')

        result2 = s.get_incident(number='INC0426232')
        inc2 = json.loads(result2.text)['result'][0]
        session_id2 = TestBase.get_cookie_by_name(s.session.cookies, 'JSESSIONID')

        self.assertEquals(inc1['number'], inc2['number'])
        self.assertEquals(inc1['short_description'], inc2['short_description'])
        self.assertEquals(session_id1, session_id2)
