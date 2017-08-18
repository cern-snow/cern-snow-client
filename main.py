import snow_object as sn

def main():
        s = sn.SnowRestSession()
	s.loadConfigFile('config.yaml')
        a = s.post(s.instance + '/oauth_token.do', None, data = {'grant_type' : 'password', 'client_id' : s.oauthClientId, 'client_secret' : s.oauthClientSecret})
        print a.text

if __name__ == '__main__':
        main()
