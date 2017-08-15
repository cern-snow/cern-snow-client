import os, subprocess, cookielib, stat, requests, json, ast, sys, numpy as np, yaml

#mettre en minuscule les item de ma classe ex: Authtype = authType ->done
#enlever underscore ->done
#enlever parenthese exterieur quand elles ne sont pas mandatory ->done
#remplacer if == Flase/True par if not ->done
#changer les sys.exit(84/0) en raise SnowRestSessionException("message")
#commenter le code avec pydoc
#enlever LE self.ConfigFile

class SnowRestSessionException(Exception):
    pass

class SnowRestSession(object):
        """docstring for SnowRestSession"""
        def __init__(self):
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

        def loadConfigFile(self, configfilepath):
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
                self.session = requests.Session()
                self.session.cookies = self.sessionCookie


        def loadTokenFile(self):
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
                            if freshCookie:
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

        def getIncident(self, incident):
            return self.get(self.instance + '/api/now/v2/table/incident?sysparm_query=number=INC' + incident)


        def __good_cookie(self):
            file = open(self.sessionCookieFile)
            a = file.read()
            if (a.find('glide_user_activity') != -1 and a.find('glide_session_store') != -1
                and a.find('glide_user_route') != -1 and a.find('JSESSIONID') != -1 and a.find('BIGipServerpool_cerntraining') != -1):
                return True
            return False

def main():
        s = SnowRestSession()
        s.loadConfigFile('config.yaml')
        a = s.getIncident('1398570')
        print a.text

if __name__ == '__main__':
        main()
