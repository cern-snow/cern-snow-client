# coding: utf-8

from cern_snow_client.session import SnowRestSession
import yaml
import os


class TestBase(object):

    basic_auth_user = 'b09313fc4f16c70015d3bc511310c719'
    sso_oauth_user = '7d480a864faa034064cc119f0310c77b'

    short_description_prefix = "snow client unit test"

    @classmethod
    def make_session(cls, config_file_path):
        s = SnowRestSession()
        s.load_config_file(config_file_path)
        return s

    @classmethod
    def make_good_basic_auth_session(cls):
        good_basic_auth_config_file = 'tests/config_files/basic_good.yaml'
        basic_auth_password = cls.get_password('basic_good')

        s = cls.make_session(good_basic_auth_config_file)
        s.set_basic_auth_password(basic_auth_password)
        return s

    @classmethod
    def make_good_sso_oauth_session(cls):
        good_sso_oauth_config_file = 'tests/config_files/sso_oauth_good.yaml'
        oauth_client_secret = cls.get_password('oauth_client_secret_good')

        s = cls.make_session(good_sso_oauth_config_file)
        s.set_oauth_client_secret(oauth_client_secret)
        return s

    @classmethod
    def get_password(cls, password_name):
        passwords_file_path = 'tests/config_files/passwords.yaml'

        with open(passwords_file_path) as f:
            passwords = yaml.safe_load(f)
            return passwords[password_name]

    @classmethod
    def get_cookie_by_name(cls, cookie_jar, cookie_name):
        for cookie in cookie_jar:
            if cookie.name == cookie_name:
                return cookie.value
        return None

    @classmethod
    def remove_basic_cookie_file(cls):
        try:
            os.remove('basic_cookie.txt')
        except OSError:
            pass

    @classmethod
    def remove_sso_oauth_cookie_token_files(cls):
        try:
            os.remove('sso_oauth_cookie.txt')
            os.remove('token_file.txt')
        except OSError:
            pass
