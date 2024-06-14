#!/usr/bin/python
# Author Ahamed Sadayan

import ndfc_auth
import json
import requests
import ndfc_credentials
import sys
import leaf_overlay_bulk_template
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

payload = leaf_overlay_bulk_template.leaf_overlay_policy
SpineNodes = ndfc_modules.get_spine_nodes(fabricName)
LeafNodes = ndfc_modules.get_leaf_nodes(fabricName)
SpineLoopback0 = ''

for node in SpineNodes:
    policy = ndfc_modules.get_switch_policy(node['serial_no'])
    for item in policy:
        if item['entityName'] == 'loopback0' and item['templateName'] == 'loopback_interface_with_tag':
            SpineLoopback0 += f"{item['nvPairs']['IP']},"

LeafSerialNos=''
for node in LeafNodes:
    LeafSerialNos += f"{node['serial_no']},"

LeafSerialNos = LeafSerialNos[:-1]
SpineLoopback0 = SpineLoopback0[:-1]

payload['nvPairs']['SPINE_IP_LIST'] = SpineLoopback0
payload['serialNumber'] = LeafSerialNos
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