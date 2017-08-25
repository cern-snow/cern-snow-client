## Synopsis
Hello, welcome on the snow-client script, the snow-client was coded in python 2.6.6, there is a main.py to complete with your requests, as well as a function.py to see the functions you can use.

## How to use it

 -First, you need a config file, you can have an easy one by using "python gen_config", after that you can use the script.
 -Second, you need to choose what you are going to do, you get do a get, put ... example below:

	s.get('url', params)
        s.getIncident('INC number')
        s.post('url', header, data)
        s.put('url', header, data)
        s.delete('url', header)

 -Third, to use the script you just have to edit the main.py like in the example below:

 	import snow_object as sn

	def main():
            s = sn.SnowRestSession()
            s.loadConfigFile('config.yaml')
            a = s.post(s.instance + '/oauth_token.do', None, data = {'grant_type' :'password', 'client_id' : s.sn.oauthClientId, 'client_secret' : s.sn.oauthClie\
ntSecret}
	    print a.text

	if __name__ == '__main__':
           main()

## Motivation

 -The motivations behind this project are: + motivation example

## Installation

on lxplus do:
   git clone https://:@gitlab.cern.ch:8443/servicenow/snow-client.git
   cd snow-client
   python gen_config
   modify the main.py
   python main.py

## Contributors

David Martin Clavo david.martin.clavo@cern.ch
James Clerc	james.clerc@cern.ch james.clerc@epitech.eu