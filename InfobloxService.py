import requests
import config
import json
import datetime

class InfobloxService:

    def __init__(self, url, username, password):
        '''
        Initializes the InfobloxService object

        :param str url: The url of the infoblox API to call Ex. dns.evertecinc.com/wapi/2.7.1/
        '''
        self.__disableWarnings()
        self.url = url
        self.username = username
        self.password = password
        self.cookie = ''


    def getObjectReference(self, recordType, record):
        '''
        '''

        parameter = self.__getParameter(recordType)

        if parameter == '':
            print('Invalid Record Type')
            return
        
        objType = 'record:' + recordType
        params = {'name': record}
        
        requestURL = self.url + objType
        
        request = self.__getRequest(requestURL, params)
        print(request.url)
        if request.status_code == 200:
            jsonData = request.json()
        
            if len(jsonData) <= 0:
                return ''
        
            return jsonData[0]['_ref']
        
        return ''
    

    def createZone(self, view, domain, dnsGroup):

        params = {}
        params['fqdn'] = domain
        params['view'] = view
        params['ns_group'] = dnsGroup
        payload = json.dumps(params)

        url = self.url + 'zone_auth'

        request = self.__postRequest(url, payload)

        print(request.text)

        if request.status_code == 201:
            return True

        return False


    def createRecord(self, recordType, domain, value, view, comment=''):
        '''
        '''

        parameter = self.__getUpdateParameter(recordType)
        data = {}
        data[parameter] = value
        data['name'] = domain
        data['view'] = view
        data['comment'] = comment
        payload = json.dumps(data)
        print(payload)

        objectType = 'record:' + recordType
        url = self.url + objectType

        request = self.__postRequest(url, payload)

        if request.status_code == 201:
            return True
        
        return False


    def updateRecord(self, objRef, recordType, record, newValue, comment=''):
        '''
        '''

        updateParam = self.__getUpdateParameter(recordType)

        if updateParam == '':
            return False

        data = {}
        data[updateParam] = newValue
        data['comment'] = comment
        payload = json.dumps(data)

        requestURL = self.url + objRef

        request = self.__putRequest(requestURL, payload)

        if request.status_code != 200:
            return False

        return True

    
    def __getUpdateParameter(self, recordType):

        if recordType == 'a' or recordType == 'A':
            return 'ipv4addr'
        elif recordType == 'cname' or recordType == 'CNAME':
            return 'canonical'
        elif recordType == 'mx' or recordType == 'MX':
            return 'mail_exchanger'
        elif recordType == 'ns' or recordType == 'NS':
            return ''
        elif recordType == 'txt' or recordType == 'TXT':
            return 'text'
        else:
            return ''


    def __getParameter(self, recordType):

        if recordType == 'a' or recordType == 'A':
            return 'name'
        elif recordType == 'cname' or recordType == 'CNAME':
            return 'canonical'
        elif recordType == 'mx' or recordType == 'MX':
            return 'mail_exchanger'
        elif recordType == 'ns' or recordType == 'NS':
            return ''
        elif recordType == 'txt' or recordType == 'TXT':
            return 'text'
        else:
            return ''

    
    def __getRequest(self, url, parameters):

        if self.cookie == '':
            request = requests.get(url, verify=False, params=parameters, auth=(self.username, self.password))
            self.__getCookie(request)
            return request

        header = {'Cookie': self.cookie}
        request = requests.get(url, verify=False, params=parameters, headers=header)
        return request

    
    def __putRequest(self, url, payload):

        if self.cookie == '':
            header = {'Content-Type': 'application/json'}
            request = requests.put(url, headers=header, verify=False, data=payload, auth=(self.username, self.password))
            self.__getCookie(request)
            return request

        header = {'Content-Type': 'application/json', 'Cookie': self.cookie}
        request = requests.put(url, headers=header,verify=False, data=payload)
        return request

    
    def __postRequest(self, url, payload):
        
        if self.cookie == '':
            header = {'Content-Type': 'application/json'}
            request = requests.post(url, headers=header, verify=False, data=payload, auth=(self.username, self.password))
            self.__getCookie(request)
            return request

        header = {'Content-Type': 'application/json', 'Cookie': self.cookie}
        request = request.post(url, headers=header, verify=False, data=payload)
        return request


    def __getCookie(self, request):

        if request.status_code == 200:
            cookies = request.cookies.get_dict()
            self.cookie = 'ibapauth=' + cookies['ibapauth']
        

    def __parseResponse(self, response):
        # Implement Record
        return

    def __disableWarnings(self):
        requests.packages.urllib3.disable_warnings()