import snow_object as sn, pydoc
import json

def main():
        s = sn.SnowRestSession()
        s.loadConfigFile('config.yaml')
	#b = s.getIncident(number='INC1441784')
	#print b.text
	#c = s.post(s.instance + '/oauth_token.do', None, data = {'grant_type' : 'password', 'client_id' : s.oauthClientId, 'client_secret' : s.oauthClientSecret})
	#print c.text
	a = s.addWorkNote(table='incident', number='INC1422216', workNote='ON EST LA')
	print a.text
	

if __name__ == '__main__':
        main()
