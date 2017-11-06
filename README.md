## Synopsis
Welcome on the snow-client library. It facilitates usage of the ServiceNow REST interface with a CERN Single Sign On account, such as a service account. Basic Authentication is also supported.

The library is compatible with Python 2.6+ but not Python 3 yet.

The library code is in the package `cern_snow_client`, and example usage is in `examples/main.py`. You should modify the configuration file `examples/config.yaml` as well.

## Motivation
* Providing a common, reliable and documented Python client library for ServiceNow users, both in the IT Department and other CERN departments
* Reducing implementation and support costs of integrations with ServiceNow at CERN

## How to use it

 * First, you need a config file. For now, please use the included example `examples/config.yaml`. The plan later on is to have a config file generation tool.
 
 * You can try the library interactively. Example below:

``` python
python
...
>>> from cern_snow_client.session import SnowRestSession
>>> s = SnowRestSession()
>>> s.load_config_file('config.yaml')
>>> s.get('https://cerntraining.service-now.com/api/now/v2/table/incident?sysparm_query=number=<number>')
>>> s.get_incident('<number>')
```

 * You can see more examples in the file `examples/main.py`.

 
**Important** : with the included example `config.yaml`, a cookie file `mycookie.txt` and a token file `mytoken.npy` will be generated as a cache to avoid reauthenticating between requests. These files have to be stored securely, as anyone with access to them could impersonate your account in ServiceNow or even another SSO-enabled CERN system. If you are just testing, be sure to delete the files after running `main.py`.

## Installation

You can clone this git repository:
``` bash
git clone https://:@gitlab.cern.ch:8443/servicenow/snow-client.git
```

You can then copy the package (folder) `cern_snow_client` into your Python project.

You can also download a .zip or .tar.gz file from this project.

## Documentation

To see the current documentation, please open the file `docs/cern_snow_client.html`

## Unit tests

While in the root of the project, please run `tests/run.sh`.
The SSO+OAuth tests will only work in an environment with the tool `cern-get-sso-cookie` (e.g. Scientific Linux CERN or CERN CentOS).
Tested environments are lxplus.cern.ch (currently Python 2.6) and aiadm (currently Python 2.7).


## Contributors

James Clerc	james.clerc@cern.ch james.clerc@epitech.eu

David Martin Clavo david.martin.clavo@cern.ch