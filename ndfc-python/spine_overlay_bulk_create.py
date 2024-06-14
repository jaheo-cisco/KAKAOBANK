#!/usr/bin/python
# Author Ahamed Sadayan

import ndfc_auth
import json
import requests
import ndfc_credentials
import sys
import spine_overlay_bulk_template
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

payload = spine_overlay_bulk_template.spine_overlay_policy
SpineNodes = ndfc_modules.get_spine_nodes(fabricName)
LeafNodes = ndfc_modules.get_leaf_nodes(fabricName)
LeafLoopback0 = ''
LeafASN=''
SpineSerialNos = ''

for node in SpineNodes:
    SpineSerialNos += f"{node['serial_no']},"
   

for node in LeafNodes:
     policy = ndfc_modules.get_switch_policy(node['serial_no'])
     for item in policy:
        if item['entityName'] == 'loopback0' and item['templateName'] == 'loopback_interface_with_tag':
              LeafLoopback0 += f"{item['nvPairs']['IP']},"
        if 'BGP_AS' in item['nvPairs']:
              if int(item['nvPairs']['BGP_AS']) > 0 and item['templateName'] == 'leaf_bgp_asn':
                 LeafASN += f"{item['nvPairs']['BGP_AS']},"

SpineSerialNos = SpineSerialNos[:-1]
LeafLoopback0 = LeafLoopback0[:-1]
LeafASN =LeafASN[:-1]



payload['nvPairs']['LEAF_IP_LIST'] = LeafLoopback0
payload['nvPairs']['LEAF_ASNS'] = LeafASN
payload['serialNumber'] = SpineSerialNos
#pprint.pprint(payload)
ndfc_token = ndfc_auth.auth(ndfc_credentials.node_ip,username,password)
headers = {'Authorization': ndfc_token, 'Content-Type': 'application/json'}


response = requests.post(posturl,
                        data=json.dumps(payload),
                        verify=False,
                        headers=headers)
pprint.pprint(payload)
print(f'response={response.text}, status_code={response.status_code}')
response.close()