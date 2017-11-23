# coding: utf-8

from record import Record
from record import RecordQuery
from task import Task

package_table = 'u_request_fulfillment'


class Request(Task):
    """
        The class Task has all the methods of the Record and Task classes,
        plus some extra methods.

        Args:
            session (SnowRestSession): a cern_snow_client.session.SnowRestSession object, which will be used
                to authenticate and communicate with ServiceNow
            values (:obj:`dict`, optional): initial values for the record

        Examples:

            Inserting a new incident:

            >>> req = Request(s)  # s is a SnowRestSession object
            >>> req.short_description = "New request"
            >>> req.u_business_service = 'e85a3f3b0a0a8c0a006a2912f2f352d1'  # Service Element "ServiceNow"
            >>> req.u_functional_element = '579fb3d90a0a8c08017ac8a1137c8ee6'  # Functional ELement "ServiceNow"
            >>> req.comments = "Initial description"
            >>> req.insert()

            Adding a comment to an incident after getting it:

            >>> req = Request(s)  # s is a SnowRestSession object
            >>> if req.get('c69bd7324fdabac07db7d3ef0310c73b'):
            >>>     req.add_comment('New comment')  # will immediately add a new comment in ServiceNow

            Resolving an Incident for which we know the number:

            >>> req = Request(s)  # s is a SnowRestSession object
            >>> req.resolve('New comment', close_code='Not authorised', key=('number', 'RQF0746626'))
        """

    def __init__(self, session, values=None):
        Record.__init__(self, session, package_table, values=values)


class RequestQuery(RecordQuery):

    def __init__(self, session):
        RecordQuery.__init__(self, session, package_table)