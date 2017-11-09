# coding: utf-8

from cern_snow_client.session import SnowRestSession
import yaml


class TestBase(object):

    short_description_prefix = "snow client unit test"

    @classmethod
    def make_session(cls, config_file_path):
        s = SnowRestSession()
        s.load_config_file(config_file_path)
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
