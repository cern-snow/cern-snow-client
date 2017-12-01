#!/usr/bin/env python
import sys
import getpass
import os

def basic_squelette(file_name='config.yaml'):
    f = open(file_name, 'w')
    f.write('instance: \nauth:\n    type: sso_oauth\n    sso_method: basic\n    user: \n    password: \nsession:\n    '
            'cookie_file: cookie.txt\nlog:\n    log_enabled: true\n    log_file_path: log.txt\n    log_level: DEBUG\n '
            '   log_format: %(asctime)s [%(name)s] [%(levelname)s] %(message)s\n    log_file_size_bytes: 1000000\n    '
            'log_file_rotations: 10\n    log_file_encoding: utf-8')
    f.close()
    print 'Generated file ' + file_name + '\n'

def kerberos_squelette(file_name='config.yaml'):
    f = open(file_name, 'w')
    f.write('instance: \nauth:\n    type: sso_oauth\n    sso_method: kerberos\n    oauth_client_id: \n    '
            'oauth_client_secret: \nsession:\n    cookie_file: cookie.txt\n    oauth_tokens_file: tokens.txt\nlog:\n  '
            '  log_enabled: true\n    log_file_path: log.txt\n    log_level: DEBUG\n    log_format: %(asctime)s [%('
            'name)s] [%(levelname)s] %(message)s\n    log_file_size_bytes: 1000000\n    log_file_rotations: 10\n    '
            'log_file_encoding: utf-8')
    f.close()
    print 'Generated file ' + file_name+ '\n'

def construct_config_file():    
    print 'Hi and welcome to the  config file generator\n'
    config_file = raw_input('Give a name to the config file (default: config.yaml)\n')
    if len(config_file) == 0:
        config_file = 'config.yaml'
    f = open(config_file, 'w')
    instance = raw_input('Set the instance (ex: cern|cerntraining|cerndev|cerntest\n')
    i = 0
    while instance != 'cern' and instance != 'cerntraining' and instance != 'cerndev' and instance != 'cerntest':
        instance = raw_input('Bad input please enter cern|cerntraining|cerndev|cerntest\n')
        i+=1
        if i == 3:
            print 'Problem in the input\n'
            sys.exit(0)
    f.write('instance : ' + instance + '.service-now.com\n')

    auth = raw_input('Set the sso_method (ex: basic|kerberos)\n')
    while auth != 'basic' and auth != 'kerberos':
        auth = raw_input('Bad input please enter basic|kerberos\n')
        i+=1
        if i == 3:
            print 'Problem in the input\n'
            sys.exit(0)
    f.write('    auth : ' + auth + '\n')

    if auth == 'basic':
        user = raw_input('Set the user\n')
        f.write('    user: ' + user + '\n')
        password = getpass.getpass('Enter your password\n')
        f.write('    password: ' + password + '\n')
    else:
        oauth_client_id = raw_input('Enter your oauth_client_id\n')
        f.write('    oauth_client_id: ' + oauth_client_id + '\n')
        oauth_client_secret = raw_input('Enter your oauth_client_secret\n')
        f.write('    oauth_client_secret: ' + oauth_client_secret + '\n')

    answer = raw_input('Do you want to Store cookie in your computer ? Y|N (highly recommended !)\n')
    i = 0
    cookie_file = None
    while answer != 'Y' and answer != 'N':
        answer = raw_input('Do you want to Store cookie in your computer ? Y|N (highly recommended !)\n')
        i+=1
        if i == 3:
            print 'Problem in the input\n'
            sys.exit(0)
    if answer == 'Y':
        cookie_file = raw_input('Enter the Name of the cookie_file (default cookie_file.txt )\n')
        if len(cookie_file) == 0:
            cookie_file = 'cookie_file.txt'
    if cookie_file is not None:
        f.write('session:\n    cookie_file: ' + cookie_file + '\n')

    if auth == 'kerberos':
        answer = raw_input('Do you want to Store Token in your computer ? Y|N (highly recommended !)\n')
        i = 0
        while answer != 'Y' and answer != 'N':
            answer = raw_input('Do you want to Store Token in your computer ? Y|N (highly recommended !)\n')
            i+=1
            if i == 3:
                print 'Problem in the input'
                sys.exit(0)
        if answer == 'Y':
            token_file = raw_input('Enter the Name of the token_file (default token_file.txt )\n')
            if len(token_file) == 0:
                token_file = 'token_file.txt'
            if cookie_file is not None:
                f.write('    oauth_tokens_file: ' + token_file + '\n')
            else:
                f.write('session:\n    oauth_token_file: ' + token_file + '\n')

    answer = raw_input('Do you want a log_file ? Y|N\n')
    i = 0
    while answer != 'Y' and answer != 'N':
        answer = raw_input('Bad input You want a log_file enter Y or N\n')
        i+=1
        if i == 3:
            print 'Problem in the input'
            sys.exit(0)
    f.close()
    
def usage():
    print 'USAGE\t./config_file_generator [-b|-k|-h]\nDESCRIPTION:'\
        '\n\t-b : create a config_file.yaml with basic configuration (-o "name of your file")' \
        '\n\t-k : create a config_file.yaml with the kerberos configuration (-o "name of your file")'

def main():
    if os.path.exists('config.yaml'):
        print 'Problem, configfile.yaml exist already'
        sys.exit(0)
    if len(sys.argv) >= 2:
        if sys.argv[1] == '-b':
            if len(sys.argv) == 4 and sys.argv[2] == '-o':
                basic_squelette(sys.argv[3])
            elif len(sys.argv) == 2:
                basic_squelette('config.yaml')
            else:
                usage()
        elif sys.argv[1] == '-k':
            if len(sys.argv) == 4 and sys.argv[2] == '-o':
                kerberos_squelette(sys.argv[3])
            elif len(sys.argv) == 2:
                kerberos_squelette('config.yaml')
            else:
                usage()
        else:
            usage()
    else:
        construct_config_file()


if __name__ == '__main__':
    main()
