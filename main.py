import snow_object as sn
def main():
        s = sn.SnowRestSession()
        s.sn.loadConfigFile('config.yaml')
        a = s.sn.post(s.instance + '/oauth_token.do', None, data = {'grant_type' : 'password', 'client_id' : s.sn.oauthClientId, 'client_secret' : s.sn.oauthClientSecret})
        print a.text

if __name__ == '__main__':
        main()
