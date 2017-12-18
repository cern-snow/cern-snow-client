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

import cookielib
import json
import os
import requests
import subprocess
import sys
import yaml
import uuid
import logging
from logging.handlers import RotatingFileHandler

try:  # Python 2.7+
    from logging import NullHandler
except ImportError:
    class NullHandler(logging.Handler):
        def emit(self, record):
            pass

from . import __version__
from common import SnowClientException


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
        self.fresh_cookie = False
        self.fresh_token = False
        self.store_cookie = True
        self.store_token = True

        self.session = requests.Session()

        self._log_enabled = False
        self._logger_name = 'snow-client.session_' + uuid.uuid4().hex[:-24]  # used to get a Logger
        self._logger = logging.getLogger(self._logger_name)
        self._log_handler = NullHandler()
        self._logger.addHandler(self._log_handler)

        self._log_file_path = None
        self._log_level = 'INFO'
        self._log_format = "%(asctime)s [%(name)s] [%(levelname)s] %(message)s"
        self._log_file_size_bytes = 1000000
        self._log_file_rotations = 10
        self._log_file_encoding = 'utf-8'

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
            self.set_instance(config_file['instance'])

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

        if 'log' in config_file:
            if 'log_enabled' in config_file['log'] and config_file['log']['log_enabled']:
                self._log_enabled = True
            if 'log_level' in config_file['log']:
                self.set_log_level(config_file['log']['log_level'])
            if 'log_file_path' in config_file['log']:
                self._log_file_path = config_file['log']['log_file_path']
            if 'log_format' in config_file['log']:
                self._log_format = config_file['log']['log_format']
            if 'log_file_size_bytes' in config_file['log']:
                self._log_file_size_bytes = config_file['log']['log_file_size_bytes']
            if 'log_file_rotations' in config_file['log']:
                self._log_file_rotations = config_file['log']['log_file_rotations']
            if 'log_file_encoding' in config_file['log']:
                self._log_file_encoding = config_file['log']['log_file_encoding']
            self._configure_handler()

    def set_instance(self, instance):
        """
        Args:
            instance (str): the ServiceNow instance to use. It is optional to prefix with "https://".
        Examples:
            >>> s = SnowRestSession()
            >>> s.set_instance("cern.service-now.com")
            >>>
            >>> s2 = SnowRestSession()
            >>> s2.set_instance("https://cerntest.service-now.com")
        """
        if not instance.startswith('https://'):
            self.instance = 'https://' + instance
        else:
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

    def set_log_enabled(self, log_enabled):
        self._log_enabled = log_enabled

    def set_log_level(self, log_level):
        self._log_level = log_level
        self._logger.setLevel(self._log_level)

    def set_log_file_path(self, log_file_path):
        self._log_file_path = log_file_path
        self._configure_handler()

    def set_log_format(self, log_format):
        self._log_format = log_format
        self._configure_handler()

    def set_log_file_size_bytes(self, log_file_size_bytes):
        self._log_file_size_bytes = log_file_size_bytes
        self._configure_handler()

    def set_log_file_rotations(self, log_file_rotations):
        self._log_file_rotations = log_file_rotations
        self._configure_handler()

    def set_log_file_encoding(self, log_file_encoding):
        self._log_file_encoding = log_file_encoding
        self._configure_handler()

    def is_logging_enabled(self):
        return self._log_enabled

    def get_logger_name(self):
        return self._logger_name

    def get_logger(self):
        return self._logger

    def get_log_handler(self):
        return self._log_handler

    def get(self, url, headers=None, params=None):
        """
        Executes a raw GET operation and returns the result.
        Used to read or retrieve information.
        The authentication method, and session cookie / OAuth tokens persistance will depend on how the session
        has been configured.

        Args:
            url (str): a relative URL, such as ``/api/now/v2/table/incident/c1c535ba85f45540adf94de5b835cd43``.
                An absolute URL such as ``https://cerntest.service-now.com/api/now/v2/table/incident/c1c535ba85f45540adf94de5b835cd43`` can also
                be used, but the instance should match with the "instance" parameter in the configuration file,
                or the value set with the ``.set_instance()`` method.
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

        Examples:
            Getting an incident by sys_id with the ServiceNow REST Table API:

            >>> s = SnowRestSession()
            >>> s.load_config_file('config.yaml')
            >>> response = s.get('/api/now/v2/table/incident/c1c535ba85f45540adf94de5b835cd43')
            >>> if response.status_code == 200:
            >>>     import json
            >>>     result = json.loads(response.text)
            >>>     if 'result' in result:
            >>>         incident = result['result']  # querying by sys_id returns a single object
            >>>         print incident['short_description']  # will print "Test" (as a unicode object)

            Getting an incident by number with the ServiceNow REST Table API:

            >>> s = SnowRestSession()
            >>> s.load_config_file('config.yaml')
            >>> response = s.get('/api/now/v2/table/incident?sysparm_query=number=INC0426232')
            >>> if response.status_code == 200:
            >>>     import json
            >>>     result = json.loads(response.text)
            >>>     if 'result' in result:
            >>>         incident_array = result['result']  # querying via an encoded query returns an array of objects
            >>>         if len(incident_array) > 0:
            >>>             incident = incident_array[0]
            >>>             print incident['short_description']  # will print "Test" (as a unicode object)
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
            url (str): a relative URL, such as ``/api/now/v2/table/incident``.
                An absolute URL such as ``https://cerntest.service-now.com/api/now/v2/table/incident`` can also
                be used, but the instance should match with the "instance" parameter in the configuration file,
                or the value set with the ``.set_instance()`` method.
            headers (:obj:`dict`, optional): any additional headers to be be passed. If not set, the 'Accept' header
                will be set to 'application/json', and 'Content' will be set to 'application/json'
            params (:obj:`dict`, optional): any additional URL parameters to be be passed
            data (str): the data that will be submitted via POST. Typically, a dictionary
                of keys and values, turned into a string with import json; json.dumps()

        Returns:
            requests.Response : If the status code is not 401, a ``requests.Response`` object is returned.
            The structure of the result inside the 'text' attribute might vary depending on the REST endpoint
            called, but typically represents the record resulting from the insert. ServiceNow may also set various
            HTTP status codes or headers in the response.

        Raises:
            SnowRestSessionException : if the operation could not be performed due to an authentication issue

        Examples:
            Inserting an incident with the ServiceNow REST Table API:

            >>> s = SnowRestSession()
            >>> s.load_config_file('config.yaml')
            >>> incident_attributes = {
            >>>    'short_description' : "New incident",
            >>>    'u_business_service' : 'e85a3f3b0a0a8c0a006a2912f2f352d1',  # Service Element "ServiceNow"
            >>>    'u_functional_element' : '579fb3d90a0a8c08017ac8a1137c8ee6',  # Functional Element "ServiceNow"
            >>>    'comments' : "Initial description"
            >>> }
            >>> import json
            >>> data = json.dumps(incident_attributes)
            >>> response = s.post('/api/now/v2/table/incident', data=data)
            >>> if response.status_code == 201:
            >>>     result = json.loads(response.text)
            >>>     if 'result' in result:
            >>>         incident = result['result']
            >>>         print incident['number']  # will print the number of the newly created incident
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
            url (str): a relative URL, such as ``/api/now/v2/table/incident/c1c535ba85f45540adf94de5b835cd43``.
                An absolute URL such as ``https://cerntest.service-now.com/api/now/v2/table/incident/c1c535ba85f45540adf94de5b835cd43`` can also
                be used, but the instance should match with the "instance" parameter in the configuration file,
                or the value set with the ``.set_instance()`` method.
            headers (:obj:`dict`, optional): any additional headers to be be passed. If not set, the 'Accept' header will be set to
                'application/json', and 'Content' will be set to 'application/json'
            params (:obj:`dict`, optional): any additional URL parameters to be be passed
            data (str): the data that will be submitted via PUT. Typically, a dictionary
                of keys and values, turned into a string with import json; json.dumps()

        Returns:
            requests.Response : If the status code is not 401, a ``requests.Response`` object is returned.
            The structure of the result inside the 'text' attribute might vary depending on the REST endpoint
            called, but typically represents the state of the record after the update.
            ServiceNow may also set various HTTP status codes or headers in the response.

        Raises:
            SnowRestSessionException : if the operation could not be performed due to an authentication issue

        Examples:
            Updating an incident with the ServiceNow REST Table API:

            >>> s = SnowRestSession()
            >>> s.load_config_file('config.yaml')
            >>> incident_attributes_to_update = {
            >>>    'watch_list' : 'david.martin.clavo@cern.ch'  # will completely replace the previous value
            >>> }
            >>> import json
            >>> data = json.dumps(incident_attributes_to_update)
            >>> response = s.put('/api/now/v2/table/incident/ca37ed334f56830015d3bc511310c7a8', data=data)
            >>> if response.status_code == 200:
            >>>     result = json.loads(response.text)
            >>>     if 'result' in result:
            >>>         incident = result['result']
            >>>         print incident['number']  # will print the number of the updated incident
            >>>         print incident['watch_list']  # will print the new value of the watch_list field
        """
        result = self.__operation(operation='put', url=url, headers=headers, params=params, data=data)
        return result

    def __call_cern_get_sso_cookie(self):
        """
        Executes the cern-get-sso-cookie command (available in CERN Linux environments)
        in order to perform a Single Sign-On and produce a cookie file.
        """
        args = ["cern-get-sso-cookie", "--reprocess", "--url", self.instance, "--outfile", self.session_cookie_file_path]
        p = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        p.wait()

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

        if not os.path.exists(self.oauth_token_file_path):  # tokens file not present. We obtain new tokens
            self.fresh_token = True
            token_request = self.session.post(self.instance + '/oauth_token.do',
                                              data={'grant_type': 'password',
                                                    'client_id': self.oauth_client_id,
                                                    'client_secret': self.oauth_client_secret})

            if token_request.status_code == 200:  # token request was successful
                self.token_dic = json.loads(token_request.text)
                if self.store_token:
                    with open(self.oauth_token_file_path, 'w') as token_file:
                        json.dump(self.token_dic, token_file)

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
                        self.token_dic = json.loads(token_request.text)
                        if self.store_token:
                            with open(self.oauth_token_file_path, 'w') as token_file:
                                json.dump(self.token_dic, token_file)
                        else:
                            raise SnowRestSessionException(
                                "SnowRestSession.__obtain_tokens: OAuth tokens could not be retrieved from ServiceNow. "
                                "Please check the OAuth client id and OAuth client secret.")

        else:  # the tokens file is present. We try to load it
            try:
                with open(self.oauth_token_file_path, 'r') as token_file:
                    self.token_dic = json.load(token_file)
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
        token_request = self.session.post(self.instance + '/oauth_token.do',
                                          data={'grant_type': 'refresh_token',
                                                'client_id': self.oauth_client_id,
                                                'client_secret': self.oauth_client_secret,
                                                'refresh_token': self.token_dic['refresh_token']})

        if token_request.status_code == 200:
            self.token_dic = json.loads(token_request.text)
            with open(self.oauth_token_file_path, 'w') as token_file:
                json.dump(self.token_dic, token_file)

        else:
            token_request = self.session.post(self.instance + '/oauth_token.do',
                                              data={'grant_type': 'password',
                                                    'client_id': self.oauth_client_id,
                                                    'client_secret': self.oauth_client_secret})
            if token_request.status_code == 200:
                self.token_dic = json.loads(token_request.text)
                with open(self.oauth_token_file_path, 'w') as token_file:
                    json.dump(self.token_dic, token_file)
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

    @staticmethod
    def __library_user_agent():
        user_agent_header = 'cern-snow-client/' + __version__
        default_headers = requests.utils.default_headers()
        if 'User-Agent' in default_headers:
            user_agent_header = user_agent_header + ' ' + default_headers['User-Agent']
        return user_agent_header

    def __execute(self, operation, url, headers=None, params=None, data=None):
        """
        Executes directly a REST Operation and returns the result

        Args:
            operation (str): either 'get', 'post' or 'put'
            url (str): a relative URL, such as "/api/now/v2/table/incident".
                An absolute URL such as "https://cerntest.service-now.com/api/now/v2/table/incident" can also
                be used, but the instance should match with the "instance" parameter in the configuration file,
                or the value set with the ``.set_instance()`` method.
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
        if not url.startswith('https://'):
            url = self.instance + url

        if not url.startswith('https://'):
            url = self.instance + url

        if not headers:
            headers = {}
        if 'User-Agent' not in headers:
            headers['User-Agent'] = self.__library_user_agent()
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
            url (str): a relative URL, such as "/api/now/v2/table/incident".
                An absolute URL such as "https://cerntest.service-now.com/api/now/v2/table/incident" can also
                be used, but the instance should match with the "instance" parameter in the configuration file,
                or the value set with the ``.set_instance()`` method.
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
                        self.token_dic = json.loads(token_request.text)
                        with open(self.oauth_token_file_path, 'w') as token_file:
                            json.dump(self.token_dic, token_file)
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
                                self.token_dic = json.loads(token_request.text)
                                with open(self.oauth_token_file_path, 'w') as token_file:
                                    json.dump(self.token_dic, token_file)
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

    def _configure_handler(self):
        self._logger.removeHandler(self._log_handler)

        file_handler_attributes_known = bool(
            self._log_file_path and self._log_file_size_bytes and self._log_file_rotations
            and self._log_file_encoding and self._log_format)

        if file_handler_attributes_known:
            self._log_handler = RotatingFileHandler(
                self._log_file_path,
                maxBytes=self._log_file_size_bytes,
                backupCount=self._log_file_rotations - 1,
                encoding=self._log_file_encoding)
            self._log_handler.setFormatter(logging.Formatter(self._log_format))

        else:
            self._log_handler = NullHandler()

        self._logger.addHandler(self._log_handler)

    def _debug(self, message):
        self._log(logging.DEBUG, message)

    def _info(self, message):
        self._log(logging.INFO, message)

    def _warning(self, message):
        self._log(logging.WARNING, message)

    def _error(self, message):
        self._log(logging.ERROR, message)

    def _critical(self, message):
        self._log(logging.CRITICAL, message)

    def _log(self, level, message):
        if self._log_enabled:
            self._logger.log(level, message)


class SnowRestSessionException(SnowClientException):
    pass
