# coding: utf-8

from record import Record
from record import RecordQuery
from cern_snow_client.common import SnowClientException

package_table = 'task'


class Task(Record):
    """
    The class Task has all the methods of the Record class,
    plus some extra methods.

    It is not possible to insert a Task, unless you specify a table_name value with a subtable.
    Alternatively, you should instantiate a subclass, such as Incident.

    Args:
        session (SnowRestSession): a cern_snow_client.session.SnowRestSession object, which will be used
            to authenticate and communicate with ServiceNow
        table_name (:obj:`str`, optional): the name of a ServiceNow table,
            e.g. 'incident', for this task
        values (:obj:`dict`, optional): initial values for the record

    Examples:
        >>> t = Task(s)  # s is a SnowRestSession object
        >>> if t.get('c1c535ba85f45540adf94de5b835cd43'):
        >>>     print t.number  # 'INC0426232'
        >>>     print t.sys_class_name  # 'incident'
        >>>     t.watch_list = 'new_value@cern.ch'
        >>>     t.update()   # updates the watch list
        >>>     t.add_comment('New comment')  # will immediately add a new comment in ServiceNow
        >>>     t.add_work_note('New work note')  # will immediately add a new work note in ServiceNow
        >>>     t.resolve('Solution text')  # will immediately resolve the incident: Incident State=Resolved,
        >>>                                 # Close Code=Restored, and a new comment/solution will be added
    """

    def __init__(self, session, table_name=package_table, values=None):
        Record.__init__(self, session, table_name, values=values)

    def add_comment(self, comment, key=None):
        """
        Adds a comment in this Task in ServiceNow.
        The comment will be sent immediately, without a need to call .update()

        Args:
            comment (str): the new comment to be added
            key (:obj:`str` or :obj:`tuple`, optional): a str the sys_id (ServiceNow unique identifier)
                of the record to update, or a tuple (field_name, field_value), such as ('number', 'INC987654').
                If this parameter is set, it will override the current sys_id of this record object, if any.

        Returns:
            bool: True if the record was updated succesfully, False otherwise.

        Raises:
            SnowClientException: if no key is provided and the current record has no ``sys_id``
            SnowRestSessionException : if there is any authentication problem

        Examples:

            Adding a comment to a task after getting it:

            >>> t = Task(s)  # s is a SnowRestSession object
            >>> if t.get('c1c535ba85f45540adf94de5b835cd43'):
            >>>     t.add_comment('New comment')  # will immediately add a new comment in ServiceNow

            Adding a comment to a task for which we know the number:

            >>> t = Task(s)  # s is a SnowRestSession object
            >>> t.add_comment('New comment', key=('number', 'INC0426232'))  # will immediately add a new comment in ServiceNow, and will download the resulting state of the task
        """

        is_key_text = isinstance(key, str) or isinstance(key, unicode)
        is_key_tuple = isinstance(key, tuple) and len(key) == 2 and isinstance(key[0], str)

        if not key and not self.sys_id:
            raise SnowClientException('Record.update: The current Record instance does not have a sys_id. '
                                      'Please provide a key to specify which record to update.')

        elif not self.sys_id and not is_key_text and not is_key_tuple:
            raise SnowClientException("Record.get: the \"key\" parameter should be a non empty str/unicode value, "
                                      "or a tuple (field_name, field_value) where field_name is a str")

        if not self.sys_class_name:
            object.__setattr__(self, 'sys_class_name', self._table_name)
        # TODO: Finish this method
        url = '/api/now/v2/table/' + self._table_name + '/'
        if key:
            if isinstance(key, tuple):
                sys_id = self.get(key)
                if sys_id is False:
                    return False
                sys_id = self.sys_id
            else:
                url = url + key
        result = self._session.get(url)

        if 'result' not in result:
            return False
        return True

    def add_work_note(self, work_note, key=None):
        """
        Similar to add_comment, but to add work notes.
        The work note will be sent immediately, without a need to call .update()

        Args:
            work_note (str): the new comment to be added
            key (:obj:`str` or :obj:`tuple`, optional): a str the sys_id (ServiceNow unique identifier)
                of the record to update, or a tuple (field_name, field_value), such as ('number', 'INC987654').
                If this parameter is set, it will override the current sys_id of this record object, if any.

        Returns:
            bool: True if the record was updated succesfully, False otherwise.

        Raises:
            SnowClientException: if no key is provided and the current record has no ``sys_id``
            SnowRestSessionException : if there is any authentication problem

        Examples:

            Adding a work note to a task after getting it:

            >>> t = Task(s)  # s is a SnowRestSession object
            >>> if t.get('c1c535ba85f45540adf94de5b835cd43'):
            >>>     t.add_work_note('New work note')  # will immediately add a new comment in ServiceNow

            Adding a comment to a task for which we know the number:

            >>> t = Task(s)  # s is a SnowRestSession object
            >>> t.add_work_note('New work note', key=('number', 'INC0426232'))  # will immediately add a new comment in ServiceNow, and will download the resulting state of the task
        """
        # TODO: Finish this method
        pass

    def resolve(self, solution, close_code=None, key=None):
        """
        Resolves a Task in ServiceNow.
        The Task will be resolved immediately, without a need to call .update()

        Args:
            solution (str): the text that will be added to the comments and which will be stored as the Solution
                of this Task
            close_code (:obj:`str`, optional): the Close Code to use. If not set, the default Close Code will be
                selected : "Restored" for Incidents and "Fulfilled" for Requests.
            key (:obj:`str` or :obj:`tuple`, optional): a str the sys_id (ServiceNow unique identifier)
                of the record to update, or a tuple (field_name, field_value), such as ('number', 'INC987654').
                If this parameter is set, it will override the current sys_id of this record object, if any.

        Returns:
            bool: True if the record was updated succesfully, False otherwise.

        Raises:
            SnowClientException: if no key is provided and the current record has no ``sys_id``
            SnowRestSessionException : if there is any authentication problem

        Examples:
            Resolving a Task after getting it:

            >>> t = Task(s)  # s is a SnowRestSession object
            >>> if t.get('c1c535ba85f45540adf94de5b835cd43'):
            >>>     t.resolve('Solution text')  # will immediately resolve in ServiceNow

            Resolving a Task for which we know the number, with close code 'Rejected':

            >>> t = Task(s)  # s is a SnowRestSession object
            >>> t.resolve('New comment', close_code='Works as designed', key=('number', 'INC0426232'))
        """

        # TODO: Finish this method
        # if an incident, make : incident_state=6, comments=solution, u_close_code=close_code
        # if a request, make : u_current_task_state=9, comments=solution, u_close_code=close_code
        # if no close_code is provided, choose 'Restored' for incident and 'Fulfilled' for request
        pass


class TaskQuery(RecordQuery):

    def __init__(self, session):
        RecordQuery.__init__(self, session, package_table)
