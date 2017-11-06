from cern_snow_client.session import SnowRestSession
import json

if __name__ == '__main__':

    s = SnowRestSession()
    s.load_config_file('example_config.yaml')

    result = s.get(
        url='https://cerntest.service-now.com/api/now/v2/table/incident?sysparm_query=number=<number>',
        headers={},
        params={}
    )
    print result.status_code
    print json.loads(result.text)

    result = s.post(
        url='https://cerntest.service-now.com/api/now/v2/table/incident',
        headers={},
        data={'field_1': 'value_1', 'field_2': 'value_2'}
    )
    print result.status_code
    print json.loads(result.text)

    result = s.put(
        url='https://cerntest.service-now.com/api/now/v2/table/incident/<sys_id>',
        headers={},
        data={'field_1': 'value_1', 'field_2': 'value_2'}
    )
    print result.status_code
    print json.loads(result.text)

    result = s.get_incident(sys_id='<sys_id>')
    result = s.get_incident(number='<number>')
    result = s.get_incidents(
        query_filter={
            'field_1': 'value_1',
            'field_2': 'value_2'
        })
    result = s.get_incidents(query_encoded='field1=value1^field2=value2')
    result = s.insert_incident(
        data={'field_1': 'value_1', 'field_2': 'value_2'})
    result = s.update_incident(
        sys_id='<sys_id>',
        data={'field_1': 'value_1', 'field_2': 'value_2'})
    result = s.update_incident(
        number='<number>',
        data={'field_1': 'value_1', 'field_2': 'value_2'})
    result = s.incident_add_comment(sys_id='<sys_id>', comment="New comment")
    result = s.incident_add_comment(number='<number>', comment="New comment")
    result = s.incident_add_work_note(sys_id='<sys_id>', work_note="New work note")
    result = s.incident_add_work_note(number='<number>', work_note="New work note")
