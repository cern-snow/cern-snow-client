# coding: utf-8

from record import Record
from record import RecordQuery
from task import Task

package_table = 'incident'


class Incident(Task):
    """
        The class Task has all the methods of the Record and Task classes,
        plus some extra methods.

        Args:
            session (SnowRestSession): a cern_snow_client.session.SnowRestSession object, which will be used
                to authenticate and communicate with ServiceNow
            values (:obj:`dict`, optional): initial values for the record

        Examples:

            Inserting a new incident:

            >>> inc = Incident(s)  # s is a SnowRestSession object
            >>> inc.short_description = "New incident"
            >>> inc.u_business_service = 'e85a3f3b0a0a8c0a006a2912f2f352d1'  # Service Element "ServiceNow"
            >>> inc.u_functional_element = '579fb3d90a0a8c08017ac8a1137c8ee6'  # Functional ELement "ServiceNow"
            >>> inc.comments = "Initial description"
            >>> inc.insert()

            Adding a comment to an incident after getting it:

            >>> inc = Incident(s)  # s is a SnowRestSession object
            >>> if inc.get('c1c535ba85f45540adf94de5b835cd43'):
            >>>     inc.add_comment('New comment')  # will immediately add a new comment in ServiceNow

            Resolving an Incident for which we know the number:

            >>> inc = Incident(s)  # s is a SnowRestSession object
            >>> inc.resolve('New comment', close_code='Not Reproducible', key=('number', 'INC0426232'))
        """

    def __init__(self, session, values=None):
        Record.__init__(self, session, package_table, values=values)


class IncidentQuery(RecordQuery):

    def __init__(self, session):
        RecordQuery.__init__(self, session, package_table)
