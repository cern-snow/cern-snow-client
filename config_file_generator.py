#!/usr/bin/env python
import sys
import getpass


def basic_squelette():
    f = open('config.yaml', 'w')
    f.write('instance: \nauth:\n    type: sso_oauth\n    sso_method: basic\n    user: \n    password: \nsession:\n    '
            'cookie_file: cookie.txt\nlog:\n    log_enabled: true\n    log_file_path: log.txt\n    log_level: DEBUG\n '
            '   log_format: %(asctime)s [%(name)s] [%(levelname)s] %(message)s\n    log_file_size_bytes: 1000000\n    '
            'log_file_rotations: 10\n    log_file_encoding: utf-8')
    f.close()


def kerberos_squelette():
    f = open('config.yaml', 'w')
    f.write('instance: \nauth:\n    type: sso_oauth\n    sso_method: kerberos\n    oauth_client_id: \n    '
            'oauth_client_secret: \nsession:\n    cookie_file: cookie.txt\n    oauth_tokens_file: tokens.txt\nlog:\n  '
            '  log_enabled: true\n    log_file_path: log.txt\n    log_level: DEBUG\n    log_format: %(asctime)s [%('
            'name)s] [%(levelname)s] %(message)s\n    log_file_size_bytes: 1000000\n    log_file_rotations: 10\n    '
            'log_file_encoding: utf-8')


def construct_config_file():
    f = open('config.yaml', 'w')
    print 'Hi and welcome to the  config file generator\n'

    instance = raw_input('Set the instance (ex: cern|cerntraining|cerndev|cerntest : ')
    i = 0
    while instance != 'cern' and instance != 'cerntraining' and instance != 'cerndev' and instance != 'cerntest':
        instance = raw_input('Bad input please enter cern|cerntraining|cerndev|cerntest: ')
        i+=1
        if i == 3:
            print 'Problem in the input'
            sys.exit(0)
    f.write('instance : ' + instance + '.service-now.com\n')

    auth = raw_input('Set the sso_method (ex: basic|kerberos): ')
    while auth != 'basic' and auth != 'kerberos':
        auth = raw_input('Bad input please enter basic|kerberos: ')
        i+=1
        if i == 3:
            print 'Problem in the input'
            sys.exit(0)
    f.write('    auth : ' + auth + '\n')

    if auth == 'basic':
        user = raw_input('Set the user')
        f.write('    user: ' + user + '\n')
        password = getpass.getpass('Enter your password: ')
        f.write('    password: ' + password + '\n')
    else:
        oauth_client_id = raw_input('Enter your oauth_client_id: ')
        f.write('    oauth_client_id: ' + oauth_client_id + '\n')
        oauth_client_secret = raw_input('Enter your oauth_client_secret: ')
        f.write('    oauth_client_secret: ' + oauth_client_secret + '\n')

    answer = raw_input('Do you want to Store cookie in your computer ? Y|N (highly recommended !) ')
    i = 0
    cookie_file = None
    while answer != 'Y' and answer != 'N':
        answer = raw_input('Do you want to Store cookie in your computer ? Y|N (highly recommended !) ')
        i+=1
        if i == 3:
            print 'Problem in the input'
            sys.exit(0)
    if answer == 'Y':
        cookie_file = raw_input('Enter the Name of the cookie_file (default cookie_file.txt ): ')
        if len(cookie_file) == 0:
            cookie_file = 'cookie_file.txt'
    if cookie_file is not None:
        f.write('session:\n    cookie_file: ' + cookie_file + '\n')

    if auth == 'kerberos':
        answer = raw_input('Do you want to Store Token in your computer ? Y|N (highly recommended !) ')
        i = 0
        while answer != 'Y' and answer != 'N':
            answer = raw_input('Do you want to Store Token in your computer ? Y|N (highly recommended !) ')
            i+=1
            if i == 3:
                print 'Problem in the input'
                sys.exit(0)
        if answer == 'Y':
            token_file = raw_input('Enter the Name of the token_file (default token_file.txt ): ')
            if len(token_file) == 0:
                token_file = 'token_file.txt'
            if cookie_file is not None:
                f.write('    oauth_tokens_file: ' + token_file + '\n')
            else:
                f.write('session:\n    oauth_token_file: ' + token_file + '\n')

    answer = raw_input('Do you want a log_file ? Y|N ')
    i = 0
    while answer != 'Y' and answer != 'N':
        answer = raw_input('Bad input You want a log_file enter Y or N: ')
        i+=1
        if i == 3:
            print 'Problem in the input'
            sys.exit(0)


def main():
    if len(sys.argv) >= 2:
        if sys.argv[1] == '-b':
            basic_squelette()
        elif sys.argv[1] == '-k':
            kerberos_squelette()
        else:
            print 'USAGE\t./config_file_generator [-b|-k|-h]\nDESCRIPTION:' \
                  '\n\t-b : create a config_file.yaml with basic configuration' \
                  '\n\t-k : create a config_file.yaml with the kerberos configuration'
    else:
        construct_config_file()


if __name__ == '__main__':
    main()
