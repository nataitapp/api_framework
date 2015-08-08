__author__ = 'nata'

import requests, json
from ConfigParser import SafeConfigParser
import time
import os
import sys


class Config:
    def __init__(self):
        #creation of object of SafeConfigParser() class to get access it's methods
        self.parser = SafeConfigParser()
        #checking if config file exists
        if os.path.isfile('config.ini'):
            self.parser.read('config.ini')
        else:
            print ('No Config.ini found under root folder.')
            sys.exit()
        #creating vars with alues from config.ini with help og 'get' method
        self.domain = self.parser.get('Server', 'domain')
        self.admin_login = self.parser.get('Server', 'admin')
        self.password = self.parser.get('Server', 'password')
        self.test_path = self.parser.get('Server', 'testpath')
#        self.puser = self.parser.get('Server', 'puser')
#        self.testdata = './test_files'

#defines the class for pretty looking response object
class Response:
    def __init__(self):
        self.http_code = 0
        self.json_body = dict()
        self.headers = dict()

#defines class to store all methods we need for this framework
class Calls:
    def __init__(self):
        #creating object of class config()
        self.config = Config()
        self.no_json = 'NO_JSON'


    def create_folder(self, name, domain = None, username = None, password = None, content_type = None, accept = None, method = None, test_path = None):
        if domain is None :
            domain = self.config.domain
        if content_type is None :
            content_type = 'application/json'
        if username is None :
            username = self.config.admin_login
        if password is None :
            password = self.config.password
        if method is None :
            method = 'POST'
        if accept is None :
            accept = 'application/json'
        if test_path is None :
            test_path = self.config.test_path


        endpoint = '/public-api/v1/fs'
        url = domain + endpoint + test_path + name
        headers = dict()
        headers['Content-Type'] = content_type
        headers['Accept'] = accept
        #body
        data = dict()
        data['action'] = 'add_folder'

        data = json.dumps(data)
        #request method returning server response to r
        r = requests.request(
            url = url,
            auth = (username, password),
            headers = headers,
            data = data,
            method = method
        )
        #first: try to parse json and convert it to python dict
        try:
            json_resp = json.loads(r.content)
        except ValueError:
            #if pasing failed then check, may be method was 'OPTIONS'
            if method == 'OPTIONS':
                json_resp = r.content
            #and finally return no-json sting to json_resp var
            else:
                json_resp = self.no_json
        #Putting processed r.content into empty r.json
        r.json = json_resp
        #creating object of class Response()
        response = Response()
        response.http_code = r.status_code
        response.json_body = r.json
        response.headers = r.headers
        return response

    def delete_folder(self, name, domain = None, username = None, password = None, content_type = None, accept = None, method = None, test_path = None):
        if domain is None :
            domain = self.config.domain
        if content_type is None :
            content_type = 'application/json'
        if username is None :
            username = self.config.admin_login
        if password is None :
            password = self.config.password
        if method is None :
            method = 'DELETE'
        if accept is None :
            accept = 'application/json'
        if test_path is None :
            test_path = self.config.test_path


        endpoint = '/public-api/v1/fs'
        url = domain + endpoint + test_path + name
        headers = dict()
        headers['Content-Type'] = content_type
        headers['Accept'] = accept


        r = requests.request(
            url = url,
            auth = (username, password),
            headers = headers,
            method = method
        )
        try:
            json_resp = json.loads(r.content)
        except ValueError:
            if method == 'OPTIONS':
                json_resp = r.content
            else:
                json_resp = self.no_json

        r.json = json_resp
        response = Response()
        response.http_code = r.status_code
        response.json_json = r.json
        response.headers = r.headers
        return response


    #defining static method(nothing to do with parent class) which generates random folder name
    @staticmethod
    def gen_random_name():
        return 'dynamic_name_%s' % str(time.time()).replace('.', '')





