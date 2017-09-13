## Synopsis
Welcome on the snow-client library. The library was coded in python 2.6.6. It facilitates usage of the ServiceNow REST interface with a CERN Single Sign On account, such as a service account.

The library code is in `snow_client.py`, and example usage in `main.py`. You should modify the example `config.yaml` as well.

## How to use it

 * First, you need a config file. For now, please use the included example `config.yaml`. The plan later on is to have a config file generation tool.
 
 * Second, you need to choose what you are going to do, you get do a get, put ... Example below:

```python
	    s.get('url', params)
        s.getIncident('INC number')
        s.post('url', header, data)
        s.put('url', header, data)
        s.delete('url', header)
```

 * Third, to use the script, you can have a look at the included example `main.py` . A very quick example:

```python
 	import snow_client

	def main():
        s = snow_client.SnowRestSession()
        s.loadConfigFile('config.yaml')
        result = s.getIncident(number='INC9876543') #changeme
	    print result.text

	if __name__ == '__main__':
        main()
```

**Important** : with the example `config.yaml` included, a cookie file `mycookie.txt` and a token file `mytoken.npy` will be generated as a cache to avoid reauthenticating between requests. These files have to be stored securely, as anyone with access to them could impersonate your account in ServiceNow or even another SSO-enabled CERN system. If you are just testing, be sure to delete the files after running `main.py`.

## Motivation
The motivations behind this project are:
* Providing a common, reliable and documented Python client library for ServiceNow users, both in the IT Department and other CERN departments
* Reducing implementation and support costs of integrations with ServiceNow at CERN

## Installation and example usage

Inside your private folder on lxplus.cern.ch, do:
``` bash
    git clone https://:@gitlab.cern.ch:8443/servicenow/snow-client.git
    cd snow-client
    #modify config.yaml as needed
    #modify main.yaml as needed
    python main.py
    rm mycookie.txt mytoken.npy
```



## Contributors

James Clerc	james.clerc@cern.ch james.clerc@epitech.eu

David Martin Clavo david.martin.clavo@cern.ch