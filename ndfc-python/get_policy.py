#!/usr/bin/python
# Author Ahamed Sadayan

import ndfc_auth
import json
import requests
import ndfc_credentials
import sys
import leaf_asn_template
import ndfc_modules
import pprint

username = ndfc_credentials.username
password = ndfc_credentials.password
url = 'https://' + ndfc_credentials.node_ip
posturl = url + f'/appcenter/cisco/ndfc/api/v1/lan-fabric/rest/control/policies/switches/FDO233804FP'

#fabricName = input('Enter the fabric name: ')
#faburl = url + f'/appcenter/cisco/ndfc/api/v1/lan-fabric/rest/control/fabrics/{fabricName}'
ndfc_token = ndfc_auth.auth(ndfc_credentials.node_ip,username,password)
headers = {'Authorization': ndfc_token, 'Content-Type': 'application/json'}
#response = requests.get(faburl, verify=False, headers=headers)
#if response.status_code != 200:
#    print(f'response code = {response.status_code}, error message = {response.text}')
#    print('Give the right Fabric Name')
#    sys.exit()



payload=''
response = requests.get(posturl,
                        data=json.dumps(payload),
                        verify=False,
                        headers=headers)
#print(f'response={response.text}, status_code={response.status_code}')
pprint.pprint(json.loads(response.text))