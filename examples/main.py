from cern_snow_client.session import SnowRestSession
from cern_snow_client.incident import Incident
from cern_snow_client.incident import IncidentQuery
from cern_snow_client.record import Record
import json

if __name__ == '__main__':

    s = SnowRestSession()
    s.load_config_file('config.yaml')

    # High level usage
    # Inserting an Incident
    new_inc = Incident(s)
    new_inc.short_description = "New incident"
    new_inc.u_business_service = 'e85a3f3b0a0a8c0a006a2912f2f352d1'  # Service Element "ServiceNow"
    new_inc.u_functional_element = '579fb3d90a0a8c08017ac8a1137c8ee6'  # Functional Element "ServiceNow"
    new_inc.comments = "Initial description"
    new_inc.incident_state = '2'  # request state = Assigned
    inserted = new_inc.insert()  # returns True/False

    # Adding a comment to an incident after getting it
    inc = Incident(s)
    if inc.get(new_inc.sys_id):
        inc.add_comment('New comment')  # will immediately add a new comment in ServiceNow

    # Resolving an Incident for which we know the number:
    inc = Incident(s)  # s is a SnowRestSession object
    inc.resolve('Solution', close_code='Not Reproducible', key=('number', new_inc.number))

    # Querying a list of Incidents
    inc_query = IncidentQuery(s)

    # Query the incidents with FE=IT Service Management Support,
    # Visibility=CERN, and already closed
    inc_list = inc_query.query(query_filter={
        'u_functional_element': 'ea56fb210a0a8c0a015a591ddbed3676',
        'u_visibility': 'cern',
        'active': 'false'
    })

    # Same query with encoded query
    inc_list = inc_query.query(
        query_encoded="u_functional_element=ea56fb210a0a8c0a015a591ddbed3676^"
                      "u_visibility=cern^active=false")
    for record in inc_list:
        print record.number + " " + record.short_description

    # Inserting a new Outage (without using the Outage class)
    otg = Record(s, 'cmdb_ci_outage')
    otg.u_publication_ssb = 'true'
    otg.u_publication_c_report = 'true'
    otg.short_description = 'Planned intervention in ServiceNow'
    otg.u_service_element = 'e85a3f3b0a0a8c0a006a2912f2f352d1'  # Service Element "ServiceNow"
    otg.u_functional_element = '579fb3d90a0a8c08017ac8a1137c8ee6'  # Functional Element "ServiceNow"
    otg.type = 'planned'
    otg.u_impact = 'degraded'
    otg.begin = '2017-11-22 14:00:00'  # UTC timezone
    otg.end = '2017-11-22 15:00:00'  # UTC timezone
    otg.u_visibility = 'cern'
    otg.u_description = "Description for the SSB"
    otg.u_publication_start_date = '2017-11-22'
    otg.u_publication_end_date = '2017-11-24'
    otg.u_technical_description = "Description for C5 report"
    otg.insert()

    # Low level usage of SnowRestSession.get , post and put
    result = s.get(
        url='/api/now/v2/table/incident?sysparm_query=number=' + new_inc.number,
        headers={},
        params={}
    )
    print result.status_code
    print json.loads(result.text)

    result = s.post(
        url='/api/now/v2/table/incident',
        headers={},
        data="{'field_1': 'value_1', 'field_2': 'value_2'}"
    )
    print result.status_code
    print json.loads(result.text)

    result = s.put(
        url='/api/now/v2/table/incident/' + new_inc.sys_id,
        headers={},
        data="{'field_1': 'value_1', 'field_2': 'value_2'}"
    )
    print result.status_code
    print json.loads(result.text)
