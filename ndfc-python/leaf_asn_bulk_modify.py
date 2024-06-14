#!/usr/bin/python
# Author Ahamed Sadayan

import ndfc_auth
import json
import requests
import ndfc_credentials
import sys
import leaf_asn_policy_modification_template
import ndfc_modules
import pprint

username = ndfc_credentials.username
password = ndfc_credentials.password
url = 'https://' + ndfc_credentials.node_ip


fabricName = input('Enter the fabric name: ')
faburl = url + f'/appcenter/cisco/ndfc/api/v1/lan-fabric/rest/control/fabrics/{fabricName}'
ndfc_token = ndfc_auth.auth(ndfc_credentials.node_ip,username,password)
headers = {'Authorization': ndfc_token, 'Content-Type': 'application/json'}
response = requests.get(faburl, verify=False, headers=headers)
if response.status_code != 200:
    print(f'response code = {response.status_code}, error message = {response.text}')
    print('Give the right Fabric Name')
    sys.exit()
policyName = input('Enter the policy name for modification: ')
if not policyName:
    print('Policy name not found, check the policy name and retry')
    sys.exit()
ASN_NUM = int(input('Enter the leaf seed 2Byte or 4 Byte ASN Number: '))
ASN_STEP = int(input('Enter the ASN increment between leaf nodes: '))
print('VPC nodes will be having the same ASN number')
LeafNodes = ndfc_modules.get_leaf_nodes(fabricName)

ASN_LIST = []
previous_serial=None
count=0
payload = leaf_asn_policy_modification_template.leaf_asn_policy
policy = ndfc_modules.get_policy(fabricName,policyName)

old_asn = 0
count = 0
for node in policy:
    posturl = url + f'/appcenter/cisco/ndfc/api/v1/lan-fabric/rest/control/policies/POLICY-{node["id"]}'
    payload_copy = payload.copy()
    if count == 0:
        payload_copy['nvPairs']['BGP_AS'] = str(ASN_NUM)
        old_asn = int(node['nvPairs']['BGP_AS'])
        count += 1
    elif count > 0 and old_asn == int(node['nvPairs']['BGP_AS']):
        payload_copy['nvPairs']['BGP_AS'] = str(ASN_NUM)
        count += 1
    elif count > 0 and old_asn != int(node['nvPairs']['BGP_AS']):
        ASN_NUM += ASN_STEP
        payload_copy['nvPairs']['BGP_AS'] = str(ASN_NUM)
        count += 1
        old_asn = int(node['nvPairs']['BGP_AS'])
    payload_copy['id'] = node["id"]
    payload_copy['policyId']=f"POLICY-{node['id']}"
    payload_copy["description"]="leaf_asn"
    payload_copy['serialNumber']=node["serialNumber"]
    payload_copy['nvPairs'] = payload['nvPairs'].copy()
    payload_copy['nvPairs']['FABRIC_NAME'] = fabricName
    payload_copy['nvPairs']['POLICY_ID'] = f'POLICY-{node["id"]}'
    ASN_LIST.append((payload_copy, posturl))




ndfc_token = ndfc_auth.auth(ndfc_credentials.node_ip,username,password)
headers = {'Authorization': ndfc_token, 'Content-Type': 'application/json'}
for value in ASN_LIST:
   payload=value[0]
   posturl=value[1]
   response = requests.put(posturl,
                            data=json.dumps(payload),
                            verify=False,
                            headers=headers)
   output = response.text
   pprint.pprint(payload)
   print(f'response={response.text}, status_code={response.status_code}')
