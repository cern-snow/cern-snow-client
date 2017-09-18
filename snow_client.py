import os, subprocess, cookielib, stat, requests, json, ast, sys, numpy as np, yaml

""" 
Hi and Welcome in the Documentation of The Snow API
"""

class SnowRestSessionException(Exception):
    """
    This is an error class for the exception
    :Exception:String
    """
    pass

class SnowRestSession(object):
    
    def __init__(self):
        """
        This is the init of the SnowRestSession class
        :return: None
        """
        self.instance = None
        self.authType = None
        self.ssoMethod = None
        self.oauthClientId = None
        self.oauthClientSecret = None
        self.sessionCookieFile = None
        self.sessionCookie = None
        self.oauthTokenFile = None
        self.tokenDic = None
        self.session = None
        self.logfile = None
        self.freshCookie = False
        self.freshToken = False
        self.storeCookie = True
        self.storeToken = True
        self.sessionCreated = False

    def loadConfigFile(self, configfilepath):
        """
        This Method load the config file and fill the variable in the class
        :return:Nothing
        """
        try:
            with open(configfilepath) as f:
                configfile = yaml.safe_load(f)
        except Exception as e:
            sys.stderr.write('SnowRestSession.loadConfigFile: Issue when opening the config file\n')
            raise e
        
        if 'instance' in configfile:
            self.instance = 'https://' + configfile['instance']
            
        if 'auth' in configfile:
            if 'type' in configfile['auth']:
                self.authType = configfile['auth']['type']
                    
            if 'sso_method' in configfile['auth']:
                self.ssoMethod = configfile['auth']['sso_method']
                
            if 'oauth_client_id' in configfile['auth']:
                self.oauthClientId = configfile['auth']['oauth_client_id']
                        
            if 'oauth_client_secret' in configfile['auth']:
                self.oauthClientSecret = configfile['auth']['oauth_client_secret']

            if 'session' in configfile:
                if 'cookie_file' in configfile['session']:
                    self.sessionCookieFile = configfile['session']['cookie_file']

            if 'oauth_tokens_file' in configfile['session']:
                self.oauthTokenFile = configfile['session']['oauth_tokens_file']

        if 'log_file' in configfile:
            self.logfile = configfile['log_file']

    def setInstance(self, instance):
        self.instance = instance
        
    def setAuthType(self, authtype):
        self.authType = authtype
        
    def setSsoMethod(self, ssomethod):
        self.ssoMethod = ssomethod

    def setOauthclientid(self, oauthclienid):
        self.oauthClientId = oauthclienid
        
    def setOauthClientSecret(self, oauthclientsecret):
        self.oauthClientSecret = oauthclientsecret

    def setSessionCookieFile(self, cookiefile):
        self.sessionCookieFile = cookiefile

    def setOauthTokenFile(self, oauthtokenfile):
        self.oauthTokenFile

    def setLogFile(self, logfile):
        self.logfile = logfile
    
    def cernGetSsoCookie(self):
        #"""Get CERN SSO cookies."""
        """
        This Methods get the cookie that connect you to the session and to the cern single sign on
        :return:Nothing but assign the cookie in a variable of self
        """
        args = ["cern-get-sso-cookie", "--reprocess", "--url", self.instance,"--outfile", self.sessionCookieFile]
        if not os.path.exists(self.sessionCookieFile):
            p = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            p.wait()
            self.freshCookie = True
        else:
            self.freshCookie = False
            if not self.__good_cookie():
                p = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                p.wait()
                self.freshCookie = True
        self.sessionCookie = cookielib.MozillaCookieJar(self.sessionCookieFile)
        self.sessionCookie.load()
        if not self.__good_cookie():
            raise SnowRestSessionException('The account used to log in does not work in ServiceNow')
        if not self.storeCookie:
            os.remove(self.sessionCookieFile)

    def requests_session(self):
        """
        This Methods creates a session and assignes cookies to the session to connect you to single sign on
        """
        if not self.sessionCreated:
            self.sessionCreated = True
            self.session = requests.Session()
        self.session.cookies = self.sessionCookie

    def loadTokenFile(self):
        """
        This Methods load the token from the token file or create them if the token file doesnt exist
        """
        if not os.path.exists(self.oauthTokenFile + '.npy'):
            self.freshToken = True
            token = self.session.post(self.instance + '/oauth_token.do', data = {'grant_type' : 'password', 'client_id' : self.oauthClientId, 'client_secret' : self.oauthClientSecret});
            if token.status_code == 200:
                self.tokenDic = ast.literal_eval(token.text)
                if self.storeToken:
                    np.save(self.oauthTokenFile, self.tokenDic)
            else:
                if self.freshCookie:
                    raise SnowRestSessionException('SnowRestSession.loadConfigFile: Issue when opening the config file')
                else:
                    self.cernGetSsoCookie()
                    self.session.cookies = self.sessionCookie
                    token = self.session.post('https://cerntraining.service-now.com/oauth_token.do', data = {'grant_type' : 'password', 'client_id' : self.oauthClientId, 'client_secret' : self.oauthClientSecret});
                    self.tokenDic = None
                    if token.status_code == 200:
                        self.tokenDic = ast.literal_eval(token.text)
                        if self.storeToken == True:
                            np.save(self.oauthTokenFile, self.tokenDic)
                        else:
                            raise SnowRestSessionException('The client id and secret might not work !')
        else:
            try:
                self.tokenDic = np.load(self.oauthTokenFile + '.npy').item()
            except:
                raise SnowRestSessionException('failed to load token file maybe bad file ?')
        
    def refreshToken(self):
        """
        This Method ask for token with the refresh token if token is expired and add them to the token file
        """
        token = self.session.post(self.instance + '/oauth_token.do', data = {'grant_type' : 'refresh_token', 'client_id' : self.oauthClientId, 'client_secret' : self.oauthClientSecret, 'refresh_token' : self.tokenDic['refresh_token']})
        if token.status_code == 200:
            self.tokenDic = ast.literal_eval(token.text)
            np.save(self.oauthTokenFile, self.tokenDic)
        else:
            token = self.session.post(self.instance + '/oauth_token.do', data = {'grant_type' : 'password', 'client_id' : self.oauthClientId, 'client_secret' : self.oauthClientSecret})
            if token.status_code == 200:
                self.tokenDic = ast.literal_eval(token.text)
                np.save(self.oauthTokenFile, self.tokenDic)
            else:
                if self.freshCookie:
                    raise SnowRestSessionException('client id and secret might not work !')

    def get(self, url, params=None):
        """
        This method retrieves multiple records for the specified table with proper pagination information.
        :url:string
        :params:dict
        """
        self.cernGetSsoCookie()
        self.requests_session()
        self.loadTokenFile()    
        result = self.session.get(url, params = None, headers = {'Authorization' : 'Bearer ' + self.tokenDic['access_token'], 'Accept' : 'application/json'})
        if result.status_code != 401:
            return result
        else:
            if self.freshToken:
                raise SnowRestSessionException('failed to load token file maybe bad file ?')
            else:
                self.refreshToken()
                token = self.session.post(self.instance + '/oauth_token.do', data = {'grant_type' : 'password', 'client_id' : self.oauthClientId, 'client_secret' : self.oauthClientSecret})
                if token.status_code == 200:
                    self.tokenDic = ast.literal_eval(token.text)
                    np.save(self.oauthTokenFile, self.tokenDic)
                    result = self.session.get(url, headers = {'Authorization' : 'Bearer ' + self.tokenDic['access_token'], 'Accept' : 'application/json'})
                    if result.status_code != 401:
                        return result
                    else:
                        raise SnowRestSessionException('Cant access to Service Now')
                else:
                    token = self.session.post(self.instance + '/oauth_token.do', data = {'grant_type' : 'password', 'client_id' : self.oauthClientId, 'client_secret' : self.oauthClientSecret})
                    if token.status_code == 200:
                        self.tokenDic = ast.literal_eval(token.text)
                        np.save(self.oauthTokenFile, self.tokenDic)
                        result = self.session.get(url, headers = {'Authorization' : 'Bearer ' + self.tokenDic['access_token'], 'Accept' : 'application/json'})
                        if result.status_code != 401:
                            return result
                        else:
                            raise SnowRestSessionException('Problem !')
                    else:
                        if self.freshCookie:
                            raise SnowRestSessionException('Problem !')
                        else:
                            os.remove(self.sessionCookieFile)
                            self.cernGetSsoCookie()
                            self.session.cookies = self.sessionCookie
                            token = self.session.post(self.instance + '/oauth_token.do', data = {'grant_type' : 'password', 'client_id' : self.oauthClientId, 'client_secret' : self.oauthClientSecret})
                            if not token.status_code == 200:
                                raise SnowRestSessionException('Problem !')
                            else:
                                self.tokenDic = ast.literal_eval(token.text)
                                np.save(self.oauthTokenFile, self.tokenDic)
                                result = self.session.get(url, headers = {'Authorization' : 'Bearer ' + self.tokenDic['access_token'], 'Accept' : 'application/json'})
                                if not result.status_code == 401:
                                    return result
                                else:
                                    raise SnowRestSessionException('Problem !')

    def post(self, url, headers=None, data=None):
        """
        This method inserts one record in the specified table. Multiple record insertion is not supported by this method.
        :url:string
        :headers:dict
        :data:dict
        """
        self.cernGetSsoCookie()
        self.requests_session()
        self.loadTokenFile()
        headers['Authorization'] = 'Bearer ' + self.tokenDic['access_token']
        post = self.session.post(url, headers=headers, data=data)
        if post.status_code == 201:
            return post
        else:
            if self.freshCookie:
                raise SnowRestSessionException('Probleme with account or with the link to put !')
            else:
                os.remove(self.sessionCookieFile)
                self.cernGetSsoCookie()
                self.session.cookies = self.sessionCookie
                if self.freshToken:
                    raise SnowRestSessionException('Probleme with account or with the link to put !')
                else:
                    os.remove(self.oauthTokenFile + '.npy')
                    self.loadTokenFile()
                    headers['Authorization'] = 'Bearer ' + self.tokenDic['access_token']
                    post = self.session.post(url, headers=headers, data=data)
                    if post.status_code == 201:
                        return post
                    else:
                        raise SnowRestSessionException('Probleme with account or with the link to put !')

    def put(self, url, headers=None, data=None):
        """
        This method updates the specified record with the request body.
        :url:string
        :headers:dict
        :data:dict
        """
        self.cernGetSsoCookie()
        self.requests_session()
        self.loadTokenFile()
        headers['Authorization'] = 'Bearer ' + self.tokenDic['access_token']
        put = self.session.put(url, headers=headers, data=data)
        if put.status_code == 200:
            return put
        else:
            if self.freshCookie:
                raise SnowRestSessionException('Problem with the account !')
            else:
                os.remove(self.sessionCookieFile)
                self.cernGetSsoCookie()
                self.session.cookies = self.sessionCookie
                put = self.session.put(url, headers=headers, data=data)
                if put.status_code == 200:
                    return put
                else:
                    os.remove(self.oauthTokenFile + '.npy')
                    self.loadTokenFile()
                    headers['Authorization'] = 'Bearer ' + self.tokenDic['access_token']
                    put = self.session.put(url, headers=headers, data=data)
                    print put.status_code
                    if put.status_code == 200:
                        return put
                    else:
                        raise SnowRestSessionException('Problem with the put request')

    def getRecord(self, table, id=None, number=None):
        # s.getRecord('incident', id='12345feab...')
        # s.getRecord('incident', number='INC12345')
        """
        The Method getRecord use the fonction get and return an object
        :return:object_get
        """
        if not table:
            raise SnowRestSessionException('getRecord needs a table value')
        url = self.instance + '/api/now/v2/table/'+ table
        if id:
            url = url + '/' + id
        elif number:
            url = url + '?sysparm_query=number=' + number
        else:
            raise SnowRestSessionException('getRecord needs at least an id or a number')
        return self.get(url)

    def getRecords(table, filter = {}, encodedQuery = ""):
        """
        The Method getRecords use the fonction get for many requests
        :return:object_get
        """
        if not table:
            raise SnowRestSessionException('getRecords needs a table value')
        url = self.instance + '/api/now/v2/table/'+ table
        if filter:
            a = []
            for key in filter:
                a.append(key + '=' + filter[key])
                encodedQuery = '^'.join(a)
        if encodedQuery:
            url = url + '?sysparm_query=' + encodedQuery
        else:
            raise SnowRestSessionException('getRecords need at least a filter or an encodedQuery')
        return self.get(url)

    def getRequest(self, id=None, number=None):
        """
        The Method getRequest is a get for request table. You give the id or the number of the request
        :return:get_object
        """
        return self.getRecord(table='u_request_fulfillment', id=id, number=number)

    def getRequests(self, filter={}, encodedQuery=""):
        """
        The Method getRequets is a get for many request.
        :return:get_object
        """
        return self.getRecords(table='u_request_fulfillment', filter=filter, encodedQuery=encodedQuery)

    def getIncidents(self, filter = {}, encodedQuery= ""):
        """
        The Method getIncidents is a get for many incident
        :return:get_object
        """
        return self.getRecord(table='incident', filter=filter, encodedQuery=encodedQuery)
        
    def getIncident(self, id=None, number=None):
        # s.getIncident(id='1213dgazd...')
        # s.getIncident(number='1367136')
        """
        The Method getIncident is a get for an incident. You give the id or the number of the incident.
        :return:get_object
        """
        return self.getRecord('incident', id=id, number=number)
        
    def insertRecord(self, table='', data={}):
        # s.insertRecord(table='incident', data=data)
        """
        This Method is using the post request to insert something in a table
        :return:post_object
        """
        if not table:
            raise SnowRestSessionException('insertRecord needs a table value')
        url = self.instance + '/api/now/v2/table/' + table
        if data:
            data = json.dumps(data)
            return self.post(url=url, headers = {'Content-Type':'application/json','Accept':'application/json'} , data=data)
        else:
            raise SnowRestSessionException('insertRecord needs a data value')

    def insertIncident(self, data):
        """
        This Method create an incident with the data you give in parameter
        :data:dict
        """
        # s.insertIncident(data=data)
        return self.insertRecord(table='incident', data=data)

    def insertRequest(self, data):
        """
        This Method create a request with the data you give in parameter
        :data:dict
        """
        # s.insertIncident(data=data)
        return self.insertRecord(table='u_request_fulfillment', data=data)

    def updateRecord(self, table=None, id=None, data={}):
        """
        This Method allow you to update any ticket
        :table:string
        :id:string
        :data:dict
        """
        # s.updateRecord('incident', id='12345feab...')
        # s.updateRecord('incident', number='INC12345')
        if not table:
            raise SnowRestSessionException('updateRecord needs a table value')
        url = self.instance + '/api/now/v2/table/' + table
        data = json.dumps(data)
        url = url + '/' + id
        return self.put(url, headers={'Content-Type':'application/json','Accept':'application/json'}, data=data)

    def updateRequest(self, id=None, number=None, data={}):
        """
        This Method allow you to update the request ticket that you want to update
        :id:string
        :number:string (RQF318....)
        :data:dict
        """
        if number:
            result = self.getRequest(number=number)
            sysid = json.loads(result.text)
            id = sysid['result'][0]['sys_id']
        if id:
            if data:
                return self.updateRecord(table='u_request_fulfillment', id=id, data=data)
        raise SnowRestSessionException('updateRequest need at least an id or a number, and a data')

    def updateIncident(self, id=None, number=None, data={}):
        """
        This Method allow you to update the incident ticket that you want to update
        :id:string
        :number:string (RQF318....)
        :data:dict
        """
        # s.updateIncident(id='12345feab...', data=data)
        # s.updateIncident(number='1234561', data=data)
        if number:
            result = self.getIncident(number=number)
            sysid = json.loads(result.text)
            id = sysid['result'][0]['sys_id']
        if id:
            if data:
                return self.updateRecord(table='incident', id=id, data=data)
        raise SnowRestSessionException('updateIncident need at least an id or a number')

    def incAddComment(self, id=None, number=None, comment=''):
        """
        This Method allow you to comment the incident ticket that you want to comment
        :id:string
        :number:string (RQF318....)
        :comment:string
        """
        if not comment:
            raise SnowRestSessionException('the comment must be not empty')
        return self.updateIncident(id=id, number=number, data={'comments' : comment})

    def reqAddComment(self, id=None, number=None, comment=''):
        """
        This Method allow you to comment the request ticket that you want to comment
        :id:string
        :number:string (RQF318....)
        :comment:string
        """
        if not comment:
            raise SnowRestSessionException('the comment must be not empty')
        return self.updateRequest(id=id, number=number, data={'comments' : comment})    

    def addComment(self, table=None, id=None, number=None, comment=''):
        """
        This Method allow you to commebt the ticket that you want to comment
        :table:string
        :id:string
        :number:string (RQF318....)
        :comment:string
        """
        if not table:
            raise SnowRestSessionException('addComment need a table')
        if number:
            result = self.getRecord(table=table, number=number)
            sysid = json.loads(result.text)
            id = sysid['result'][0]['sys_id']
        if not id:
            raise SnowRestSessionException('You must specified an id or a number')
        if not comment:
            raise SnowRestSessionException('the comment must be not empty')
        return self.updateRecord(table=table, id=id, data={'comments': comment})

    def reqAddWorkNote(self, id=None, number=None, workNote=''):
        """
        This Method allow you to add a worknote on the request ticket that you want
        :id:string
        :number:string (RQF318....)
        :workNote:string
        """
        if not workNote:
            raise SnowRestSessionException('the comment must be not empty')
        return self.updateRequest(id=id, number=number, data={'work_notes' : workNote})

    def incAddWorkNote(self, id=None, number=None, workNote=''):
        """
        This Method allow you to add a worknote on the incident ticket that you want
        :id:string
        :number:string (RQF318....)
        :workNote:string
        """
        if not workNote:
            raise SnowRestSessionException('the comment must be not empty')
        return self.updateIncident(id=id, number=number, data={'work_notes' : workNote})

    def addWorkNote(self, table=None, id=None, number=None, workNote=''):
        """
        This Method allow you to add a worknote on the ticket that you want
        :table:string
        :id:string
        :number:string (RQF318....)
        :workNote:string
        """
        if not table:
            raise SnowRestSessionException('addWorkNote need a table')
        if number:
            result = self.getRecord(table=table, number=number)
            sysid = json.loads(result.text)
            id = sysid['result'][0]['sys_id']
        if not id:
            raise SnowRestSessionException('You must specified an id or a number')
        if not workNote:
            raise SnowRestSessionException('the comment must be not empty')
        return self.updateRecord(table=table, id=id, data={'work_notes': workNote})

    def __good_cookie(self):
        file = open(self.sessionCookieFile)
        a = file.read()
        if (a.find('glide_user_activity') != -1 and a.find('glide_session_store') != -1 and a.find('glide_user_route') != -1 and a.find('JSESSIONID') != -1 and a.find('BIGipServerpool_cerntraining') != -1):
            return True
        return False
