# coding: utf-8

import ast
import cookielib
import json
import numpy as np
import os
import requests
import subprocess
import sys
import yaml


class SnowRestSession(object):
    """
    This class behaves very similarly to a requests.Session object.
    It can be configured by loading a .yaml config file,
    or by setting attributes.
    """

    def __init__(self):
        self.instance = None
        self.auth_type = None
        self.sso_method = None
        self.basic_auth_user = None
        self.basic_auth_password = None
        self.oauth_client_id = None
        self.oauth_client_secret = None
        self.session_cookie_file_path = None
        self.session_cookie = None
        self.oauth_token_file_path = None
        self.token_dic = None
        self.logfile = None
        self.fresh_cookie = False
        self.fresh_token = False
        self.store_cookie = True
        self.store_token = True
        self.log_file_path = None

        self.session = requests.Session()

    def load_config_file(self, config_file_path):
        """
        Load a .yaml configuration file

        Args:
            config_file_path (str): the path to the configuration file

        Raises:
            SnowRestSessionException: if no file is found at the specified path, or some inconsistency is found
                in the file.
            Exception: if some other error happens when opening or parsing the file
        """
        if not config_file_path:
            raise SnowRestSessionException(
                "SnowRestSession.load_config_file: the parameter config_file_path must have a value")

        try:
            with open(config_file_path) as f:
                config_file = yaml.safe_load(f)
        except Exception as e:
            sys.stderr.write(
                "SnowRestSession.load_config_file: Issue when opening the config file at %s.\n" % config_file_path)
            raise e

        if 'instance' in config_file:
            self.instance = 'https://' + config_file['instance']

        if 'auth' in config_file:
            if 'type' in config_file['auth']:
                self.auth_type = config_file['auth']['type']

        if self.auth_type == 'sso_oauth':
            if 'sso_method' in config_file['auth']:
                self.sso_method = config_file['auth']['sso_method']

            if 'oauth_client_id' in config_file['auth']:
                self.oauth_client_id = config_file['auth']['oauth_client_id']

            if 'oauth_client_secret' in config_file['auth']:
                self.oauth_client_secret = config_file['auth']['oauth_client_secret']

            if 'session' in config_file:
                if 'cookie_file' in config_file['session']:
                    self.session_cookie_file_path = config_file['session']['cookie_file']

            if 'oauth_tokens_file' in config_file['session']:
                self.oauth_token_file_path = config_file['session']['oauth_tokens_file']

        elif self.auth_type == 'basic':
            if 'user' in config_file['auth']:
                self.basic_auth_user = config_file['auth']['user']

            if 'password' in config_file['auth']:
                self.basic_auth_password = config_file['auth']['password']

            if 'session' in config_file:
                if 'cookie_file' in config_file['session']:
                    self.session_cookie_file_path = config_file['session']['cookie_file']
        else:
            raise SnowRestSessionException(
                "SnowRestSession.load_config_file: the property \"auth_type\" "
                "must have a value of \"sso_auth\" or \"basic\"")

        if 'log_file_path' in config_file:
            self.log_file_path = config_file['log_file_path']

    def set_instance(self, instance):
        """
        Args:
            instance (str): the ServiceNow instance to use. Example: '\https://cern.service-now.com'
        """
        self.instance = instance

    def set_auth_type(self, auth_type):
        """
        Args:
            auth_type (str): the authentication type to use. Either 'sso_auth' or 'basic'

        Raises:
            SnowRestSessionException: if auth_type is not 'sso_auth' or 'basic'
        """
        if auth_type != 'basic' and auth_type != 'sso_auth':
            raise SnowRestSessionException(
                "SnowRestSession.set_auth_type: the parameter \"auth_type\" "
                "must have a value of \"sso_auth\" or \"basic\"")
        self.auth_type = auth_type

    def set_sso_method(self, sso_method):
        """
        Args:
            sso_method (str): the Single Sign On method to use. Either 'kerberos' or 'certificate'.
            Needs set_auth_type('sso_auth') to have an effect.

        Raises:
            SnowRestSessionException: if sso_method is not 'kerberos' or 'certificate'

        Note: certificate support needs to be implemented
        """
        if sso_method != 'kerberos' and sso_method != 'certificate':
            raise SnowRestSessionException(
                "SnowRestSession.set_sso_method: the parameter \"sso_method\" "
                "must have a value of \"kerberos\" or \"certificate\"")

        # TODO: implement certificate support. Update the comment above
        if sso_method == 'certificate':
            raise SnowRestSessionException("SnowRestSession.set_sso_method: certificate support is not yet implemented")
        self.sso_method = sso_method

    def set_oauth_client_id(self, oauth_client_id):
        """
        Args:
            oauth_client_id (str): the OAuth client id provided to you by your instance's ServiceNow administrator.
            Needs set_auth_type('sso_auth') to have an effect.
        """
        self.oauth_client_id = oauth_client_id

    def set_oauth_client_secret(self, oauth_client_secret):
        """
        Args:
            oauth_client_secret (str): the OAuth client secret provided to you by your instance's
            ServiceNow administrator.
            Needs set_auth_type('sso_auth') to have an effect.
            An OAuth client secret is sensitive information; please store it as securely as possible.
        """
        self.oauth_client_secret = oauth_client_secret

    def set_session_cookie_file_path(self, session_cookie_file_path):
        """
        Args:
            session_cookie_file_path (str): the path to the file where the session cookies will be persisted.
            If not provided, the cookies will not be persisted.
        """
        self.session_cookie_file_path = session_cookie_file_path

    def set_oauth_token_file_path(self, oauth_token_file_path):
        """
        Args:
            oauth_token_file_path (str): the path to the file where the OAuth refresh and access tokens
            will be persisted. If not provided, the OAuth tokens will not be persisted.
        """
        self.oauth_token_file_path = oauth_token_file_path

    def set_log_file_path(self, log_file_path):
        """
        Args:
            log_file_path (str): the path to the log file

        Note: logging to a file needs to be implemented
        """
        # TODO: implement a log file
        self.log_file_path = log_file_path

    def set_basic_auth_user(self, basic_auth_user):
        """
        Args:
            basic_auth_user (str): the name of the local ServiceNow account that will be used for authentication.
            Needs set_auth_type('basic') to have an effect.
        """
        self.basic_auth_user = basic_auth_user

    def set_basic_auth_password(self, basic_auth_password):
        """
        Args:
            basic_auth_password (str): the password of the local ServiceNow account that will be used for
            authentication.
            Needs set_auth_type('basic') to have an effect.
        """
        self.basic_auth_password = basic_auth_password

    def __call_cern_get_sso_cookie(self):
        """
        Executes the cern-get-sso-cookie command (available in CERN Linux environments)
        in order to perform a Single Sign-On and produce a cookie file.
        """
        args = ["cern-get-sso-cookie", "--reprocess", "--url", self.instance, "--outfile", self.session_cookie_file_path]
        p = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        p.wait()

    def __cern_get_sso_cookie(self):
        """
        Loads and checks an existing cookie file, in order to avoid logging into ServiceNow and the
        CERN Single-Sign-On if possible. If needed, logs in again into both to produce the cookie file.
        The cookie file is loaded into memory.
        If not needed to persist the cookie file, it is deleted.

        Raises:
            SnowRestSessionException: if the Single Sign On login is not succesful. This is determined by parsing
                the cookie file after it is produced.
        """

        if not os.path.exists(self.session_cookie_file_path):  # cookie file not present. We perform Single Sign On
            self.__call_cern_get_sso_cookie()
            self.fresh_cookie = True

        else:  # cookie file present. We check if it has the correct format
            self.fresh_cookie = False
            if not self.__good_cookie():  # the format is bad. We create a new cookie file
                self.__call_cern_get_sso_cookie()
                self.fresh_cookie = True

        # we load the cookie file
        self.session_cookie = cookielib.MozillaCookieJar(self.session_cookie_file_path)
        self.session_cookie.load()

        # we check if the log in was sucessful
        if not self.__good_cookie():
            raise SnowRestSessionException(
                "SnowRestSession.__cern_get_sso_cookie: The current account has failed to perform "
                "a Single-Sign-On login in to ServiceNow")

        # we load the cookies into the requests.Session session
        self.session.cookies = self.session_cookie

        # if not needed to persist the cookie file, we delete it
        if not self.store_cookie:
            os.remove(self.session_cookie_file_path)

    def __obtain_tokens(self):
        """
        Loads the OAuth access and refresh tokens from the token file.
        If the token file is not present, new OAuth access and refresh tokens are obtained.

        Raises:
            SnowRestSessionException: if the OAuth tokens could not be retrieved from ServiceNow.
            IOError, ValueError: if the token file could not be opened
        """

        if not os.path.exists(self.oauth_token_file_path + '.npy'):  # tokens file not present. We obtain new tokens
            self.fresh_token = True
            token_request = self.session.post(self.instance + '/oauth_token.do',
                                              data={'grant_type': 'password',
                                                    'client_id': self.oauth_client_id,
                                                    'client_secret': self.oauth_client_secret})

            if token_request.status_code == 200:  # token request was successful
                self.token_dic = ast.literal_eval(token_request.text)
                if self.store_token:
                    np.save(self.oauth_token_file_path, self.token_dic)

            else:  # token request failed. Possibly, an existing cookie file contained a timed out session
                if self.fresh_cookie:  # we just performed a Single-Sign-On. There is a problem with token retrieval.
                    raise SnowRestSessionException(
                        "SnowRestSession.__obtain_tokens: OAuth tokens could not be retrieved from ServiceNow. "
                        "Please check the OAuth client id and OAuth client secret.")

                else:  # we may need to perform Single-Sign-On again, as the session may have timed out
                    self.__cern_get_sso_cookie()
                    token_request = self.session.post(self.instance + '/oauth_token.do',
                                                      data={'grant_type': 'password',
                                                            'client_id': self.oauth_client_id,
                                                            'client_secret': self.oauth_client_secret})
                    self.token_dic = None
                    if token_request.status_code == 200:
                        self.token_dic = ast.literal_eval(token_request.text)
                        if self.store_token:
                            np.save(self.oauth_token_file_path, self.token_dic)
                        else:
                            raise SnowRestSessionException(
                                "SnowRestSession.__obtain_tokens: OAuth tokens could not be retrieved from ServiceNow. "
                                "Please check the OAuth client id and OAuth client secret.")

        else:  # the tokens file is present. We try to load it
            try:
                self.token_dic = np.load(self.oauth_token_file_path + '.npy').item()
            except (IOError, ValueError) as e:
                sys.stderr.write(
                    "SnowRestSession.__obtain_tokens: Issue when opening "
                    "the token file at %s.\n" % self.oauth_token_file_path)
                raise e

    def __initiate_session(self):
        """
        Initiates a session via CERN Single-Sign-On + OAuth, or basic Authentication

        Raises:
            SnowRestSessionException: if auth_type is not 'sso_auth' nor 'basic'
        """
        if self.auth_type == 'sso_oauth':
            self.__cern_get_sso_cookie()
            self.__obtain_tokens()

        elif self.auth_type == 'basic':
            self.session.auth = (self.basic_auth_user, self.basic_auth_password)
            self.session.cookies = cookielib.MozillaCookieJar()
            if os.path.exists(self.session_cookie_file_path):
                self.session.cookies.load(self.session_cookie_file_path, ignore_discard=True, ignore_expires=True)

        else:
            raise SnowRestSessionException(
                "SnowRestSession.__initiate_session: self.auth_type "
                "has a value different from \"basic\" and \"sso_auth\"")

    def __refresh_token(self):
        """
        Requests an OAuth access token via the OAUTH refresh token.
        Saves the resulting access token in the token file.

        Raises:
            SnowRestSessionException: if the access token could not be obtained
        """
        token = self.session.post(self.instance + '/oauth_token.do',
                                  data={'grant_type': 'refresh_token',
                                        'client_id': self.oauth_client_id,
                                        'client_secret': self.oauth_client_secret,
                                        'refresh_token': self.token_dic['refresh_token']})

        if token.status_code == 200:
            self.token_dic = ast.literal_eval(token.text)
            np.save(self.oauth_token_file_path, self.token_dic)

        else:
            token = self.session.post(self.instance + '/oauth_token.do',
                                      data={'grant_type': 'password',
                                            'client_id': self.oauth_client_id,
                                            'client_secret': self.oauth_client_secret})
            if token.status_code == 200:
                self.token_dic = ast.literal_eval(token.text)
                np.save(self.oauth_token_file_path, self.token_dic)
            else:
                if self.fresh_cookie:
                    raise SnowRestSessionException(
                        "SnowRestSession.__refresh_token: the OAuth client id and OAuth secret might not be valid")

    def __save_cookie_basic(self):
        """
        Persists the basic authentication cookie file.
        """
        self.fresh_cookie = True
        self.session.cookies.save(self.session_cookie_file_path, ignore_discard=True, ignore_expires=True)

    def __execute(self, operation, url, headers=None, params=None, data=None):
        """
        Executes directly a REST Operation and returns the result

        Args:
            operation (str): either 'get', 'post' or 'put'
            url (str): an absolute URL
            headers (:obj:`dict`, optional): any additional headers to be be passed. This method will add
                Accept:application/json and Content-Type:application/json if not specified.
                It will also add the Authorization header if the authentication type is 'sso_auth',
                by setting it to the OAuth access header.
            params (:obj:`dict`, optional): any additional URL parameters to be be passed
            data (object): the data to be sent in a post or put operation

        Returns:
            requests.Response

        Raises:
            SnowRestSessionException: if the operation parameter is not 'get', 'post' or 'put'

        """
        if not operation:
            raise SnowRestSessionException("SnowRestSession.__execute: the operation paramater is mandatory")
        if not url:
            raise SnowRestSessionException("SnowRestSession.__execute: the url paramater is mandatory")

        if not headers:
            headers = {}
        if 'Accept' not in headers:
            headers['Accept'] = 'application/json'
        if (operation == 'post' or operation == 'put') and 'Content-Type' not in headers:
            headers['Content-Type'] = 'application/json'
        if self.auth_type == 'sso_oauth':
            headers['Authorization'] = 'Bearer ' + self.token_dic['access_token']

        if operation == 'get':
            result = self.session.get(url, headers=headers, params=params)
        elif operation == 'post':
            result = self.session.post(url, headers=headers, params=params, data=data)
        elif operation == 'put':
            result = self.session.put(url, headers=headers, params=params, data=data)
        else:
            raise SnowRestSessionException("SnowRestSession.__execute: the operation paramater "
                                           "needs to be either \"get\", \"post\" or \"put\"")

        return result

    def __operation(self, operation, url, headers=None, params=None, data=None):
        """
        Executes a REST Operation, taking care of reauthenticating if needed, and returns the result

        Args:
            operation (str): either 'get', 'post' or 'put'
            url (str): an absolute URL
            headers (:obj:`dict`, optional): any additional headers to be be passed. If not set, some headers will be set by
                default (see __execute method)
            params (:obj:`dict`, optional): any additional URL parameters to be be passed
            data (object): the data to be sent in a post or put operation

        Returns:
            requests.Response : if the status code is not 401, a requests.Response object is returned

        Raises:
            SnowRestSessionException : if the operation could not be performed due to an authentication issue
        """
        self.__initiate_session()

        result = self.__execute(operation, url, headers=headers, params=params, data=data)

        if result.status_code != 401:
            if self.auth_type == 'basic':
                self.__save_cookie_basic()
            return result

        else:
            if self.auth_type == 'basic':
                if not self.fresh_cookie:
                    self.session.auth = (self.basic_auth_user, self.basic_auth_password)
                    result = self.__execute(operation, url, headers=headers, params=params, data=data)
                    if result.status_code != 401:
                        self.__save_cookie_basic()
                        return result
                    else:
                        raise SnowRestSessionException(
                            "SnowRestSession.__operation: Your basic authentication "
                            "user and password might not be valid")
                else:
                    raise SnowRestSessionException(
                        "SnowRestSession.__operation: Your basic authentication "
                        "user and password might not be valid")

            elif self.auth_type == 'sso_auth':

                if self.fresh_token:
                    raise SnowRestSessionException(
                        "SnowRestSession.__operation: failed to perform the operation. The current account might not "
                        "be able to log in to ServiceNow or the OAuth client id and secret might not be valid")

                else:
                    self.__refresh_token()
                    token_request = self.session.post('post', self.instance + '/oauth_token.do',
                                                      data={'grant_type': 'password',
                                                            'client_id': self.oauth_client_id,
                                                            'client_secret': self.oauth_client_secret})
                    if token_request.status_code == 200:
                        self.token_dic = ast.literal_eval(token_request.text)
                        np.save(self.oauth_token_file_path, self.token_dic)
                        headers['Authorization'] = 'Bearer ' + self.token_dic['access_token']
                        result = self.__execute(operation, url, headers=headers, params=params, data=data)
                        if result.status_code != 401:
                            return result
                        else:
                            raise SnowRestSessionException(
                                "SnowRestSession.__operation: failed to perform the operation. "
                                "The current account might not be able to log in to ServiceNow or "
                                "the OAuth client id and secret might not be valid")

                    else:
                        if self.fresh_cookie:
                            raise SnowRestSessionException(
                                "SnowRestSession.__operation: OAuth tokens could not be retrieved from ServiceNow. "
                                "Please check the OAuth client id and OAuth client secret.")
                        else:
                            os.remove(self.session_cookie_file_path)
                            self.__cern_get_sso_cookie()
                            token_request = self.session.post('post', self.instance + '/oauth_token.do',
                                                              data={'grant_type': 'password',
                                                                    'client_id': self.oauth_client_id,
                                                                    'client_secret': self.oauth_client_secret})
                            if token_request.status_code == 401:
                                raise SnowRestSessionException(
                                    "SnowRestSession.__operation: OAuth tokens could not be retrieved from ServiceNow. "
                                    "Please check the OAuth client id and OAuth client secret.")
                            else:
                                self.token_dic = ast.literal_eval(token_request.text)
                                np.save(self.oauth_token_file_path, self.token_dic)
                                headers['Authorization'] = 'Bearer ' + self.token_dic['access_token']
                                result = self.__execute(operation, url, headers=headers, params=params,
                                                        data=data)
                                if result.status_code != 401:
                                    return result
                                else:
                                    raise SnowRestSessionException(
                                        "SnowRestSession.__operation: failed to perform the operation. "
                                        "The current account might not be able to log in to ServiceNow or "
                                        "the OAuth client id and secret might not be valid")
            else:
                raise SnowRestSessionException(
                    "SnowRestSession.__operation: self.auth_type has a value different from \"basic\" and \"sso_auth\"")

    def get(self, url, headers=None, params=None):
        """
        Executes a raw GET operation and returns the result.
        Used to read or retrieve information.
        The authentication method, and session cookie / OAuth tokens persistance will depend on how the session
        has been configured.

        Args:
            url (str): an absolute URL
            headers (:obj:`dict`, optional): any additional headers to be be passed. If not set, the 'Accept' header will be set to
                'application/json'
            params (:obj:`dict`, optional): any additional URL parameters to be be passed

        Returns:
            requests.Response : If the status code is not 401, a ``requests.Response`` object is returned.
            The structure of the result inside the 'text' attribute might vary depending on the REST endpoint
            called and the way that the query is configured. ServiceNow may also set various HTTP status codes
            or headers in the response.

        Raises:
            SnowRestSessionException : if the operation could not be performed due to an authentication issue
        """
        result = self.__operation(operation='get', url=url, headers=headers, params=params)
        return result

    def post(self, url, headers=None, params=None, data=None):
        """
        Executes a raw POST operation and returns the result.
        Used to insert records or other information.
        The authentication method, and session cookie / OAuth tokens persistance will depend on how the session
        has been configured.

        Args:
            url (str): an absolute URL
            headers (:obj:`dict`, optional): any additional headers to be be passed. If not set, the 'Accept' header will be set to
                'application/json', and 'Content' will be set to 'application/json'
            params (:obj:`dict`, optional): any additional URL parameters to be be passed
            data (object): the data that will be submitted via POST. For example, a dictionary of keys and values.

        Returns:
            requests.Response : If the status code is not 401, a ``requests.Response`` object is returned.
            The structure of the result inside the 'text' attribute might vary depending on the REST endpoint
            called, but typically represents the record resulting from the insert. ServiceNow may also set various
            HTTP status codes or headers in the response.

        Raises:
            SnowRestSessionException : if the operation could not be performed due to an authentication issue
        """
        result = self.__operation(operation='post', url=url, headers=headers, params=params, data=data)
        return result

    def put(self, url, headers=None, params=None, data=None):
        """
        Executes a raw PUT operation and returns the result.
        Used to update records or other information.
        The authentication method, and session cookie / OAuth tokens persistance will depend on how the session
        has been configured.

        Args:
            url (str): an absolute URL
            headers (:obj:`dict`, optional): any additional headers to be be passed. If not set, the 'Accept' header will be set to
                'application/json', and 'Content' will be set to 'application/json'
            params (:obj:`dict`, optional): any additional URL parameters to be be passed
            data (object): the data that will be submitted via PUT. For example, a dictionary of keys and values.

        Returns:
            requests.Response : If the status code is not 401, a ``requests.Response`` object is returned.
            The structure of the result inside the 'text' attribute might vary depending on the REST endpoint
            called, but typically represents the state of the record after the update.
            ServiceNow may also set various HTTP status codes or headers in the response.

        Raises:
            SnowRestSessionException : if the operation could not be performed due to an authentication issue
        """
        result = self.__operation(operation='put', url=url, headers=headers, params=params, data=data)
        return result

    def get_record(self, table, sys_id=None, number=None, headers=None, params=None):
        """
        Executes a GET operation in order to read a single record from a ServiceNow table.
        The authentication method, and session cookie / OAuth tokens persistance will depend on how the session
        has been configured.

        Args:
            table (str): the name of a ServiceNow table, such as ``incident``. Mandatory parameter.
            sys_id (str): the sys_id (ServiceNow unique identifier) of the record to be read.
                Giving either a `sys_id` or a `number` parameter is mandatory, but not both.
            number (str): the number of the record to be read. Can be used if the table has a Number field.
                Giving either a `sys_id` or a `number` parameter is mandatory, but not both.
            headers (:obj:`dict`, optional): any additional headers to be be passed. If not set, the 'Accept' header will be set to
                'application/json'.
            params (:obj:`dict`, optional): any additional URL parameters to be be passed. For a complete list, please see:
                https://docs.servicenow.com/bundle/helsinki-application-development/page/integrate/inbound-rest/concept/c_TableAPI.html#ariaid-title3

        Returns:
            requests.Response : If the status code is not 401, a ``requests.Response`` object is returned.
                The 'text' will contain a JSON or XML representation of the record.
                The response will also contain headers. For a list of headers, please see:
                https://docs.servicenow.com/bundle/helsinki-application-development/page/integrate/inbound-rest/concept/c_TableAPI.html#d45069e608

        Raises:
            SnowRestSessionException : if mandatory parameters are missing,
                or if the operation could not be performed due to an authentication issue
        """

        if not table:
            raise SnowRestSessionException("SnowRestSession.get_record: the table paramater needs a non empty value")
        if not sys_id and not number:
            raise SnowRestSessionException("SnowRestSession.get_record: "
                                           "needs either a value in the sys_id or the number parameters")

        url = self.instance + '/api/now/v2/table/' + table
        if sys_id:
            url = url + '/' + sys_id
        elif number:
            url = url + '?sysparm_query=number=' + number

        return self.get(url=url, headers=headers, params=params)

    def get_records(self, table=None, query_filter=None, query_encoded=""):
        """
        The Method get_records use the fonction get for many requests
        :param table:
        :param query_filter:
        :param query_encoded:
        :return:object_get
        """
        if not table:
            raise SnowRestSessionException("SnowRestSession.get_records: the table paramater needs a non empty value")
        if not query_filter and not query_encoded:
            raise SnowRestSessionException("SnowRestSession.get_record: "
                                           "needs either a value in the query_filter or the query_encoded parameters")

        url = self.instance + '/api/now/v2/table/' + table
        if query_filter:
            a = []
            for key in query_filter:
                a.append(key + '=' + query_filter[key])
                query_encoded = '^'.join(a)
        if query_encoded:
            url = url + '?sysparm_query=' + query_encoded

        return self.get(url=url)

    def get_request(self, sys_id=None, number=None):
        """
        The Method getRequest is a get for request table. You give the id or the number of the request
        :return:get_object
        """
        return self.get_record(table='u_request_fulfillment', sys_id=sys_id, number=number)

    def get_requests(self, query_filter=None, query_encoded=""):
        """
        The Method getRequets is a get for many request.
        :return:get_object
        """
        return self.get_records(table='u_request_fulfillment', query_filter=query_filter, query_encoded=query_encoded)

    def get_incidents(self, query_filter=None, query_encoded=""):
        """
        The Method getIncidents is a get for many incident
        :return:get_object
        """
        return self.get_records(table='incident', query_filter=query_filter, query_encoded=query_encoded)

    def get_incident(self, sys_id=None, number=None):
        """
        The Method get_incident is a get for an incident. You give the id or the number of the incident.
        :return:get_object
        """
        return self.get_record(table='incident', sys_id=sys_id, number=number)

    def insert_record(self, table=None, data=None):
        """
        This Method is using the post request to insert something in a table
        :return:post_object
        """
        if not table:
            raise SnowRestSessionException("SnowRestSession.insert_record: the table paramater needs a non empty value")
        if not data:
            raise SnowRestSessionException("SnowRestSession.insert_record: the data paramater needs a non empty value")

        url = self.instance + '/api/now/v2/table/' + table

        data = json.dumps(data)

        return self.post(url=url, data=data)

    def insert_incident(self, data):
        """
        This Method create an incident with the data you give in parameter
        :data:dict
        """
        return self.insert_record(table='incident', data=data)

    def insert_request(self, data):
        """
        This Method create a request with the data you give in parameter
        :data:dict
        """
        return self.insert_record(table='u_request_fulfillment', data=data)

    def update_record(self, table=None, sys_id=None, data=None):
        """
        This Method allow you to update any ticket
        :table:string
        :sys_id:string
        :data:dict
        """
        if not table:
            raise SnowRestSessionException("SnowRestSession.update_record: the table paramater needs a non empty value")
        if not data:
            raise SnowRestSessionException("SnowRestSession.update_record: the data paramater needs a non empty value")

        url = self.instance + '/api/now/v2/table/' + table
        data = json.dumps(data)
        url = url + '/' + sys_id

        return self.put(url=url, data=data)

    def update_request(self, sys_id=None, number=None, data=None):
        """
        This Method allow you to update the request ticket that you want to update
        :sys_id:string
        :number:string (RQF318....)
        :data:dict
        """
        if not sys_id and not number:
            raise SnowRestSessionException("SnowRestSession.update_request: "
                                           "needs either a value in the sys_id or the number parameters")
        if number:
            result = self.get_request(number=number)
            result_object = json.loads(result.text)
            sys_id = result_object['result'][0]['sys_id']

        return self.update_record(table='u_request_fulfillment', sys_id=sys_id, data=data)

    def update_incident(self, sys_id=None, number=None, data=None):
        """
        This Method allow you to update the incident ticket that you want to update
        :sys_id:string
        :number:string (RQF318....)
        :data:dict
        """
        if not sys_id and not number:
            raise SnowRestSessionException("SnowRestSession.update_incident: "
                                           "needs either a value in the sys_id or the number parameters")

        if number:
            result = self.get_incident(number=number)
            result_object = json.loads(result.text)
            sys_id = result_object['result'][0]['sys_id']

        return self.update_record(table='incident', sys_id=sys_id, data=data)

    def incident_add_comment(self, sys_id=None, number=None, comment=None):
        """
        This Method allow you to comment the incident ticket that you want to comment
        :sys_id:string
        :number:string (RQF318....)
        :comment:string
        """
        return self.add_comment(table='incident', sys_id=sys_id, number=number, comment=comment)

    def request_add_comment(self, sys_id=None, number=None, comment=None):
        """
        This Method allow you to comment the request ticket that you want to comment
        :sys_id:string
        :number:string (RQF318....)
        :comment:string
        """
        return self.add_comment(table='u_request_fulfillment', sys_id=sys_id, number=number, comment=comment)

    def add_comment(self, table=None, sys_id=None, number=None, comment=None):
        """
        This Method allow you to commebt the ticket that you want to comment
        :table:string
        :sys_id:string
        :number:string (RQF318....)
        :comment:string
        """
        if not table:
            raise SnowRestSessionException("SnowRestSession.add_comment: the table parameter is mandatory")
        if not sys_id and not number:
            raise SnowRestSessionException("SnowRestSession.add_comment: "
                                           "needs either a value in the sys_id or the number parameters")
        if not comment:
            raise SnowRestSessionException("SnowRestSession.add_comment: the comment parameter is mandatory")

        if number:
            result = self.get_record(table=table, number=number)
            result_object = json.loads(result.text)
            sys_id = result_object['result'][0]['sys_id']

        return self.update_record(table=table, sys_id=sys_id, data={'comments': comment})

    def request_add_work_note(self, sys_id=None, number=None, work_note=''):
        """
        This Method allow you to add a worknote on the request ticket that you want
        :sys_id:string
        :number:string (RQF318....)
        :work_note:string
        """
        return self.add_work_note(table='incident', sys_id=sys_id, number=number, work_note=work_note)

    def incident_add_work_note(self, sys_id=None, number=None, work_note=''):
        """
        This Method allow you to add a worknote on the incident ticket that you want
        :sys_id:string
        :number:string (RQF318....)
        :work_note:string
        """
        return self.add_work_note(table='u_request_fulfillment', sys_id=sys_id, number=number, work_note=work_note)

    def add_work_note(self, table=None, sys_id=None, number=None, work_note=''):
        """
        This Method allow you to add a worknote on the ticket that you want
        :table:string
        :sys_id:string
        :number:string (RQF318....)
        :work_note:string
        """
        if not table:
            raise SnowRestSessionException("SnowRestSession.add_work_note: the table parameter is mandatory")
        if not sys_id and not number:
            raise SnowRestSessionException("SnowRestSession.add_work_note: "
                                           "needs either a value in the sys_id or the number parameters")
        if not work_note:
            raise SnowRestSessionException("SnowRestSession.add_work_note: the work_note parameter is mandatory")

        if number:
            result = self.get_record(table=table, number=number)
            result_object = json.loads(result.text)
            sys_id = result_object['result'][0]['sys_`id']

        return self.update_record(table=table, sys_id=sys_id, data={'work_notes': work_note})

    def __good_cookie(self):
        cookie_file = open(self.session_cookie_file_path)
        cookie_file_contents = cookie_file.read()

        if (
                cookie_file_contents.find('glide_user_activity') != -1 and
                cookie_file_contents.find('glide_session_store') != -1 and
                cookie_file_contents.find('glide_user_route') != -1 and
                cookie_file_contents.find('JSESSIONID') != -1 and
                cookie_file_contents.find('BIGipServerpool_cern') != -1
        ):
            return True

        return False


class SnowRestSessionException(Exception):
    pass
