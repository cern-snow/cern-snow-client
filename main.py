import snow_object as sn, pydoc

def main():
        s = sn.SnowRestSession()
        s.loadConfigFile('config.yaml')
	#s.getLog()
	#c = s.post(s.instance + '/oauth_token.do', None, data = {'grant_type' : 'password', 'client_id' : s.oauthClientId, 'client_secret' : s.oauthClientSecret})
	#print c.text
	a = s.insertRecord('incident', data = {"u_business_service" : "e85a376e0a0a8c0a004ca384c6043fe1", "u_functional_element" : "ea56f72a0a0a8c0a010f2fddfd8e0a68", "assignment_group" : "ea56f7310a0a8c0a001b376fe5aa9cc6", "short_description" : "test new incident by REST", "comments" : "test comments" })
	print a.text

if __name__ == '__main__':
        main()
