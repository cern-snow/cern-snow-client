# coding: utf-8

from common import SnowClientException, TableClassMapping

import abc
import inspect
import json
import re


class SessionAware(object):
    __metaclass__ = abc.ABCMeta

    def __init__(self, session):
        self._session = session

    def _debug(self, message):
        self._session._debug(message)

    def _info(self, message):
        self._session._info(message)

    def _warning(self, message):
        self._session._warning(message)

    def _error(self, message):
        self._session._error(message)

    def _critical(self, message):
        self._session._critical(message)


class Record(SessionAware):
    """
    Represents a record in a ServiceNow table.
    Attributes of the record can be set with str values.
    When getting values of the attributes, they will be of the RecordField class. See the ``get``

    Args:
        session (SnowRestSession): a cern_snow_client.session.SnowRestSession object, which will be used
            to authenticate and communicate with ServiceNow
        table_name (str): the name of a ServiceNow table, e.g. 'incident', that this object will represent
        values (:obj:`dict`, optional): initial values for the record

    Raises:
        SnowClientException : if any of the parameters is set incorrectly

    Examples:

        Building a new Record for the table 'incident':

        >>> r = Record(s, 'incident')  # s is a SnowRestSession object

        Building and initializing a new Record for the table 'u_request_fulfillment':

        >>> values = {
        >>>    'short_description' : "New request",
        >>>    'u_business_service' : 'e85a3f3b0a0a8c0a006a2912f2f352d1', #  Service Element "ServiceNow"
        >>>    'u_functional_element' : '579fb3d90a0a8c08017ac8a1137c8ee6',  # Functional Element "ServiceNow"
        >>>    'comments' : "Initial description",
        >>>    'u_current_task_state' : '2'  # initial state : Assigned
        >>> }
        >>> r = Record(s, 'u_request_fulfillment', values)  # record is created and ready for insert
    """

    def __init__(self, session, table_name=None, values=None):

        if not session:
            raise SnowClientException('Record.__init__: To create a Record instance'
                                      'you need to provide a non-empty SnowRestSession object.')
        if not table_name:
            raise SnowClientException('Record.__init__: To create a Record instance'
                                      'you need to provide a table_name value.')
        if values and type(values) is not dict:
            raise SnowClientException('Record.__init__: the values parameter needs to be a dict.')

        super(Record, self).__init__(session)

        self._table_name = table_name

        table_class_mapping = TableClassMapping.get()
        if table_name in table_class_mapping:
            self._can_insert = table_class_mapping[table_name]['can_be_inserted']
        else:
            self._can_insert = True

        self.sys_id = None
        self.sys_class_name = None

        if values:
            self._changes = values
            self._set_values(values)
        else:
            self._changes = {}

        self._initialized = True

    def __setattr__(self, key, value):
        initialized = hasattr(self, '_initialized') and self._initialized

        if key == 'sys_id' and hasattr(self, 'sys_id') and self.sys_id:
            raise SnowClientException("Record.__setattr__: the field ``sys_id`` is read-only if it already has a value")
        if initialized and key == 'sys_class_name':
            raise SnowClientException("Record.__setattr__: the field ``sys_class_name`` is read-only")

        if not key.startswith('_'):
            value = RecordField(value)

        if initialized and not key.startswith('_'):
            self._changes[key] = value

        object.__setattr__(self, key, value)

    def _set_values(self, values):
        for key in values:
            # protect private attributes
            if key.startswith('_'):
                continue
            # protect methods
            elif key in dir(self) and inspect.ismethod(self.__getattribute__(key)):
                continue

            value = RecordField(values[key])

            object.__setattr__(self, key, value)

    def get(self, key):
        """
        Fetches from ServiceNow a record from the table specified in the constructor via the argument ``table_name``.
        The record may be fetched by its ``sys_id`` (ServiceNow unique identifier), or with a (field_name, field_value)
        pair.
        The attributes of the Record will be of the RecordField class, which behaves like a unicode value
        (thanks to inheriting from unicode)

        Args:
            key (:obj:`str`, :obj:`unicode` or :obj:`tuple`): a str/unicode value with the sys_id (ServiceNow unique identifier)
                of the record to fetch; or a tuple (field_name, field_value), such as ('number', 'INC987654')

        Returns:
            bool: True if a record was fetched succesfully, False if the record did not exist

        Raises:
            SnowClientException: if the ``key`` argument is invalid.
            SnowRestSessionException : if there is any authentication problem

        Examples:
            Getting an incident by sys_id:

            >>> r = Record(s, 'incident')  # s is a SnowRestSession object
            >>> if r.get('c1c535ba85f45540adf94de5b835cd43'):
            >>>
            >>>     # short_description is a String field in ServiceNow
            >>>     print r.short_description  # 'Test'
            >>>     print r.short_description.get_value()  # 'Test'
            >>>     print r.short_description.get_display_value()  # 'Test'
            >>>     print r.short_description.is_reference()  # False
            >>>
            >>>     # u_functional_element is a Reference field in ServiceNow
            >>>     print r.u_functional_element  # 'ea56fb210a0a8c0a015a591ddbed3676', the sys_id of the Functional Element "IT Service Management Support"
            >>>     print r.u_functional_element.get_value()  # 'ea56fb210a0a8c0a015a591ddbed3676'
            >>>     print r.u_functional_element.get_display_value()  # 'IT Service Management Support'
            >>>     print r.u_functional_element.is_reference()  # True
            >>>     print r.u_functional_element.get_referenced_table()  # 'u_cmdb_ci_functional_services'
            >>>
            >>>     # incident_state is a Choice field in ServiceNow
            >>>     print r.incident_status  # 7
            >>>     print r.incident_status.get_value()  # 7
            >>>     print r.incident_status.get_display_value()  # 'Closed'
            >>>     print r.incident_status.is_reference()  # False

            Getting a request by number:

            >>> r = Record(s, 'u_request_fulfillment')  # s is a SnowRestSession object
            >>> if r.get(('number', 'RQF0746626')):
            >>>     print r.short_description
        """
        self._info("Record.get: Obtaining a record in table " + repr(self._table_name) + ' with key = ' + repr(key))

        is_key_text = isinstance(key, str) or isinstance(key, unicode)
        is_key_tuple = isinstance(key, tuple) and len(key) == 2 and isinstance(key[0], str)

        if not key or (not is_key_text and not is_key_tuple):
            raise SnowClientException("Record.get: the \"key\" parameter should be a non empty str/unicode value, "
                                      "or a tuple (field_name, field_value) where field_name is a str")
        # TODO: Finish this method
        url = '/api/now/v2/table/' + self._table_name
        if is_key_text:
            url = url + '/' + key
        elif is_key_tuple:
            url = url + '?sysparm_query=' + key[0] + '=' + key[1]
        
        #  build the URL
        result = self._session.get(url=url, params={'sysparm_display_value': 'all'})
        #  execute a get
        result = json.loads(result.text)
        #  parse the JSON result
        if is_key_text:
            if 'result' not in result:
                return False
            result = result['result']
        elif is_key_tuple:
            if not result['result']:
                return False
            result = result['result'][0]
        #  set the values inside the current object : _set_values()
        self._set_values(result)
        #  return True or False
        return True

    def insert(self):
        """
        Inserts in ServiceNow a record into the table specified in the constructor via the argument ``table_name``.
        After inserting, the attributes of the Record object will be updated with the resulting values from ServiceNow.

        Returns:
            bool: True if the record was inserted succesfully, False otherwise.

        Raises:
            SnowClientException: if the current record is of a table where records cannot be inserted
                Example: the ``task`` table is a `supertable` of ``incident`` and ``u_request_fulfillment``.
                Incidents and requests can be inserted, but not tasks who are neither an incident nor a request.

            SnowRestSessionException : if there is any authentication problem

        Examples:

            Passing the values in the constructor:

            >>> r = Record(s, 'incident', {  # s is a SnowRestSession object
            >>>    'short_description' : "New incident",
            >>>    'u_business_service' : 'e85a3f3b0a0a8c0a006a2912f2f352d1',  # Service Element "ServiceNow"
            >>>    'u_functional_element' : '579fb3d90a0a8c08017ac8a1137c8ee6',  # Functional Element "ServiceNow"
            >>>    'comments' : "Initial description",
            >>>    'incident_state' : '2'  # initial state : Assigned
            >>> })
            >>> r.insert()
            >>> print r.number  # will print the number of the new incident

            Setting values in the fields after instantiating the class:

            >>> r = Record(s, 'u_request_fulfillment')  # s is a SnowRestSession object
            >>> r.short_description = "New request"
            >>> r.u_business_service = 'e85a3f3b0a0a8c0a006a2912f2f352d1'  # Service Element "ServiceNow"
            >>> r.u_functional_element = '579fb3d90a0a8c08017ac8a1137c8ee6'  # Functional ELement "ServiceNow"
            >>> r.comments = "Initial description"
            >>> r.u_current_task_state = '2'   # request state = Assigned
            >>> r.insert()
        """

        if not self._can_insert:
            class_name = type(self).__name__
            raise SnowClientException('Record.insert: The current Record is of class ' + class_name + ', '
                                      'which cannot be inserted. '
                                      'You need to instantiate a subclass of ' + class_name + '.')
        # TODO: Finish this method
        #  build the URL
        url = '/api/now/v2/table/' + self._table_name
        #  execute a post using the changed data : get_changed_fields()
        data = json.dumps(self._changes)
        result = self._session.post(url=url, data=data, params={'sysparm_display_value': 'all'})
        #  parse the JSON result
        result = json.loads(result.text)
        self.reset_changed_values()
        if 'result' not in result:
            return False
        #  reset the changed data : reset_changed_values()
        #  set the values inside the current object: _set_values()
        self._set_values(result['result'])
        #  return True or False
        return True

    def update(self, key=None):
        """
        Updates a record in ServiceNow.
        This can be done in a record previously obtained with a get operation, or previously inserted,
        or also on a record where its table and sys_id (or key) are previously known.
        Only the changes in the fields since the last ``.insert()`` or ``.update()`` will be sent.
        After updating, the attributes of the Record object will be updated with the resulting values from ServiceNow.

        Args:
            key (:obj:`str`, :obj:`unicode` or :obj:`tuple`, optional): a str/unicode value with the sys_id
                (ServiceNow unique identifier) of the record to update; or a tuple (field_name, field_value),
                such as ('number', 'INC987654').
                If this parameter is set, it will override the current sys_id of this record object, if any.

        Returns:
            bool: True if the record was updated succesfully, False otherwise.

        Raises:
            SnowClientException: if no key is provided and the current record has no ``sys_id``
            SnowRestSessionException : if there is any authentication problem

        Examples:

            Getting an incident and then updating it:

            >>> r = Record(s, 'incident'), {  # s is a SnowRestSession object
            >>> if r.get(('number', 'INC0426232')):
            >>>    if r.watch_list:
            >>>        r.watch_list = r.watch_list + ','
            >>>    r.watch_list = r.watch_list + 'david.martin.clavo@cern.ch'
            >>>    r.update()
            >>>    print r.watch_list  # will print the new value of the watchlist, where the above address might
            >>>                        # have been replaced by the user's sys_id

            Updating a previously known incident:

            >>> r = Record(s, 'incident')  # s is a SnowRestSession object
            >>> r.watch_list = 'david.martin.clavo@cern.ch'  # will completely replace the previous value
            >>> r.update(('number', 'INC0426232'))
            >>> print r.short_description  # will print the incident's short description, since all fields are returned
            >>>                            # by ServiceNow
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
        #  build the URL (using self.sys_class_name as table)

        #  execute a put using the changed data : get_changed_fields()

        #  parse the JSON result

        #  reset the changed data : reset_changed_values()

        #  set the values inside the current object: _set_values()

        #  return True or False

    def get_changed_fields(self):
        """
        Returns:
            dict: A dictionary ``{'field_name' : 'field_value'}`` with the record fields which have changed
            since the last ``.insert()`` or ``.update()``
        """
        return self._changes

    def reset_changed_values(self):
        """
        Resets the changes in the record fields since the last ``.insert()`` or ``.update()``
        """
        self._changes = {}

    def get_session(self):
        """
        Returns:
            SnowRestSession : The session that this Record object uses to communicate with ServiceNow
        """
        return self._session

    def get_table_name(self):
        """
        Returns:
            str : The table_name argument that was used to build this Record object.
            Might be different from self.sys_class_name.

        Examples:

            >>> r = Record(s, 'task'), {  # s is a SnowRestSession object
            >>> if r.get(('number', 'INC0426232')):
            >>>     print r.get_table_name  # will print 'task'
            >>>     print r.sys_class_name   # will print 'incident'
        """
        return self._table_name

    def get_can_insert(self):
        """
        Returns:
            bool: If the current record is of a table where records cannot be inserted
            Example: the ``task`` table is a `abstract supertable` of ``incident`` and ``u_request_fulfillment``.
            Records can be inserted in the ``incident`` and ``u_request_fulfillment`` tables, but not in ``task``.
        """
        return self._can_insert


class RecordField(unicode):
    """
    Represents a ServiceNow table field.
    While a ServiceNow String field only has a value, other fields may have a different value and display value.
    For example, in an incident which is in state "In progress", the ``incident_state`` field has a display value
    of ``In Progress`` but a value of ``3``.
    Similarly, in an incident with Functional Element=ServiceNow, the Functional Element field will have a display value
    of ``ServiceNow`` but a value of ``579fb3d90a0a8c08017ac8a1137c8ee6`` : the `sys_id` of that Functional Element.

    Examples:

        >>> r = Record(s, 'incident')  # s is a SnowRestSession object
        >>> if r.get('c1c535ba85f45540adf94de5b835cd43'):
        >>>
        >>>     # short_description is a String field in ServiceNow
        >>>     print r.short_description  # 'Test'
        >>>     print r.short_description.get_value()  # 'Test'
        >>>     print r.short_description.get_display_value()  # 'Test'
        >>>     print r.short_description.is_reference()  # False
        >>>
        >>>     # u_functional_element is a Reference field in ServiceNow
        >>>     print r.u_functional_element  # 'ea56fb210a0a8c0a015a591ddbed3676', the sys_id of the Functional Element "IT Service Management Support"
        >>>     print r.u_functional_element.get_value()  # 'ea56fb210a0a8c0a015a591ddbed3676'
        >>>     print r.u_functional_element.get_display_value()  # 'IT Service Management Support'
        >>>     print r.u_functional_element.is_reference()  # True
        >>>     print r.u_functional_element.get_referenced_table()  # 'u_cmdb_ci_functional_services'
        >>>
        >>>     # incident_state is a Choice field in ServiceNow
        >>>     print r.incident_status  # 7
        >>>     print r.incident_status.get_value()  # 7
        >>>     print r.incident_status.get_display_value()  # 'Closed'
        >>>     print r.incident_status.is_reference()  # False
    """

    table_in_link_pattern = None

    def __new__(cls, value, encoding='utf-8', errors='strict'):

        if isinstance(value, dict):
            if 'value' in value:
                return cls.__build_unicode_from_value(value['value'], encoding, errors)
            elif 'display_value' in value:
                return cls.__build_unicode_from_value(value['display_value'], encoding, errors)
            else:
                return super(RecordField, cls).__new__(cls)
        else:
            return cls.__build_unicode_from_value(value, encoding, errors)

    @classmethod
    def __build_unicode_from_value(cls, value, encoding, errors):
        if isinstance(value, unicode):
            return super(RecordField, cls).__new__(cls, value)

        elif isinstance(value, str):
            return super(RecordField, cls).__new__(cls, value, encoding, errors)

        else:
            return super(RecordField, cls).__new__(cls, value)

    def __init__(self, value, encoding='utf-8', errors='strict'):

        self.__value = u''
        self.__display_value = u''
        self.__is_reference = False
        self.__referenced_table = None

        if isinstance(value, unicode):
            self.__value = value
            self.__display_value = self.__value

        elif isinstance(value, str):
            self.__value = unicode(value, encoding, errors)
            self.__display_value = self.__value

        elif type(value) is dict:

            if 'value' in value:
                inner_value = value['value']
                if isinstance(inner_value, unicode):
                    self.__value = inner_value
                elif isinstance(inner_value, str):
                    self.__value = unicode(inner_value, encoding, errors)
                else:
                    self.__value = unicode(inner_value)

            if 'display_value' in value:
                display_value = value['display_value']
                if isinstance(display_value, unicode):
                    self.__display_value = display_value
                elif isinstance(display_value, str):
                    self.__display_value = unicode(display_value, encoding, errors)
                else:
                    self.__display_value = unicode(display_value)

            if 'value' in value and 'display_value' not in value:
                self.__display_value = self.__value
            elif 'display_value' in value and 'value' not in value:
                self.__value = self.__display_value

            if 'link' in value:
                link = value['link']
                pattern = self.__get_table_in_link_re()
                match = pattern.search(link)
                if match:
                    matched_value = match.group(1)
                    if matched_value:
                        if isinstance(matched_value, unicode):
                            self.__is_reference = True
                            self.__referenced_table = matched_value
                        elif isinstance(matched_value, str):
                            self.__is_reference = True
                            self.__referenced_table = unicode(matched_value, encoding, errors)

        else:
            self.__value = unicode(value)
            self.__display_value = self.__value

    def get_value(self):
        """
        Returns:
            unicode : The internal value of the field. For choice or reference fields, such as Incident State or
            Functional Element, the internal value might be different from the display value.
        """
        return self.__value

    def get_display_value(self):
        """
        Returns:
            unicode: The display value of the field, i.e. what a user sees in the ServiceNow web UI.
        """
        return self.__display_value

    def is_reference(self):
        """
        Returns:
            bool: True if this field is a reference field (reference to another table), False otherwise.
        """
        return self.__is_reference

    def get_referenced_table(self):
        """
        Returns:
            unicode: If this field is a reference field, the internal name of the table referenced by it.
        """
        return self.__referenced_table

    @classmethod
    def __get_table_in_link_re(cls):
        if not cls.table_in_link_pattern:
            cls.table_in_link_pattern = re.compile('/table/([\w_]+)/')
        return cls.table_in_link_pattern


class RecordQuery(SessionAware):
    """
    A class to perform get queries that returns one or more records.

    Args:
        session (SnowRestSession): a cern_snow_client.session.SnowRestSession object, which will be used
            to authenticate and communicate with ServiceNow
        table_name (str): the name of a ServiceNow table, e.g. 'incident', from which to query from

    Raises:
        SnowClientException : if any of the parameters is set incorrectly
    """

    def __init__(self, session, table_name=None):
        if not session:
            raise SnowClientException('RecordQuery.__init__: To create a RecordQuery instance'
                                      'you need to provide a non-empty SnowRestSession object.')
        if not table_name:
            raise SnowClientException('RecordQuery.__init__: To create a RecordQuery instance'
                                      'you need to provide table_name value.')

        super(RecordQuery, self).__init__(session)
        self._table_name = table_name

    def query(self, query_filter=None, query_encoded=None):
        """
        Executes the query.
        At least a `query_filter` or `query_encoded` parameter need to be provided.

        Args:
            query_filter (dict): a dictionary with field names and values. Only records where the fields have
                the corresponding values will be returned
            query_encoded (str): a ServiceNow encoded query.
                See https://docs.servicenow.com/bundle/helsinki-servicenow-platform/page/use/using-lists/concept/c_EncodedQueryStrings.html

        Returns:
            RecordSet : A RecordSet object, which is an iterable, and which will return in each iteration
            an instance of the class corresponding to the ``table_name`` provided in the constructor, if available;
            otherwise, an instance of the Record class.
        """

        if not query_filter and not query_encoded:
            raise SnowClientException("RecordQuery.query: "
                                      "needs either a value in the query_filter or the query_encoded parameters")
        # TODO: Finish this method
        #  build the URL

        #  execute a get

        #  build an array of objects where each object represents a record

        #  build a RecordSet passing the array

        #  return the RecordSet

    def get_session(self):
        """
        Returns:
            SnowRestSession : The session that this RecordQuery object uses to communicate with ServiceNow
        """
        return self._session

    def get_table_name(self):
        """
        Returns:
            str : The table_name argument that was used to build this RecordQuery object.
        """
        return self._table_name


class RecordSet(SessionAware):

    def __init__(self, session, result_array, table_name):
        super(RecordSet, self).__init__(session)
        self._result_array = result_array
        self._table_name = table_name

        table_class_mapping = TableClassMapping.get()
        if table_name in table_class_mapping:
            self._record_class = table_class_mapping[table_name]['class']
        else:
            self._record_class = Record

    def __iter__(self):
        self.n = 0
        return self

    def next(self):
        """
        Returns:
            Record : An instance of Record or of a subclass of Record.
        """

        if self.n < len(self._result_array):
            record_dict = self._result_array[self.n]
            record = self._record_class(self._session, values=record_dict)
            self.n += 1
            return record

        else:
            raise StopIteration

    def get_session(self):
        """
        Returns:
            SnowRestSession : The session that this RecordSet object uses to communicate with ServiceNow
        """
        return self._session

    def get_table_name(self):
        """
        Returns:
            str : The table_name argument that was used to build this RecordSet object.
            All the records contained inside this RecordSet might belong to this table, or to a child table.
        """
        return self._table_name

    def get_record_class(self):
        """
        Returns:
            type : The Python class (Task, Incident...) that is used to build the objects returned by ``next()``
        """
        return self._record_class
