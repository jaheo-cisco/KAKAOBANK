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
posturl = url + f'/appcenter/cisco/ndfc/api/v1/lan-fabric/rest/control/policies/bulk-create'

fabricName = input('Enter the fabric name: ')
faburl = url + f'/appcenter/cisco/ndfc/api/v1/lan-fabric/rest/control/fabrics/{fabricName}'
ndfc_token = ndfc_auth.auth(ndfc_credentials.node_ip,username,password)
headers = {'Authorization': ndfc_token, 'Content-Type': 'application/json'}
response = requests.get(faburl, verify=False, headers=headers)
if response.status_code != 200:
    print(f'response code = {response.status_code}, error message = {response.text}')
    print('Give the right Fabric Name')
    sys.exit()
ASN_NUM = int(input('Enter the leaf seed 2Byte or 4 Byte ASN Number: '))
ASN_STEP = int(input('Enter the ASN increment between leaf nodes: '))
print('VPC nodes will be having the same ASN number')
LeafNodes = ndfc_modules.get_leaf_nodes(fabricName)

ASN_LIST = []
previous_serial=None
count=0
payload = leaf_asn_template.leaf_asn_policy
for node in LeafNodes:
  if node['vpc'] == True and node['peer_serial_no'] == previous_serial:
     payload_copy = payload.copy()
     payload_copy['nvPairs'] = payload['nvPairs'].copy()
     payload_copy['nvPairs']['BGP_AS']=str(ASN_NUM)
     payload_copy['serialNumber'] += f',{node["serial_no"]}'
     ASN_LIST.append(payload_copy)
  elif node['vpc'] == True and count == 0:
     payload['serialNumber'] = node["serial_no"]
     previous_serial = node['serial_no']
  elif node['vpc'] == True and count > 0 and node['peer_serial_no'] != previous_serial:
     ASN_NUM += ASN_STEP
     payload['serialNumber'] = node["serial_no"]
     previous_serial = node['serial_no']
  elif not node['vpc'] and count == 0:
     payload_copy = payload.copy()
     payload_copy['serialNumber'] = node["serial_no"]
     payload_copy['nvPairs'] = payload['nvPairs'].copy()
     payload_copy['nvPairs']['BGP_AS'] = str(ASN_NUM)
     print(ASN_NUM)
     previous_serial = node['serial_no']
     count += 1
     ASN_LIST.append(payload_copy)
  elif not node['vpc'] and count > 0:
     payload_copy = payload.copy()
     ASN_NUM += ASN_STEP
     payload_copy['serialNumber'] = node["serial_no"]
     payload_copy['nvPairs'] = payload['nvPairs'].copy()
     payload_copy['nvPairs']['BGP_AS'] = str(ASN_NUM)
     print(ASN_NUM)
     previous_serial = node['serial_no']
     ASN_LIST.append(payload_copy)





print('\n----------------------\n')
#pprint.pprint(ASN_LIST)
#sys.exit()
payload = leaf_asn_template.leaf_asn_policy
ndfc_token = ndfc_auth.auth(ndfc_credentials.node_ip,username,password)
headers = {'Authorization': ndfc_token, 'Content-Type': 'application/json'}
for value in ASN_LIST:
   payload=value
   response = requests.post(posturl,
                            data=json.dumps(payload),
                            verify=False,
                            headers=headers)
   pprint.pprint(payload)
   print(f'response={response.text}, status_code={response.status_code}')