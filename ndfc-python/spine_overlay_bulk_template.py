#!/usr/bin/python
# Author Ahamed Sadayan
# Template for http post leaf ASN policy for BGP fabric
# After import make changes to the relevant field


spine_overlay_policy = {"nvPairs":{"LEAF_IP_LIST":"1.1.1.1,1.1.1.2,2.0.5.1",
                                   "LEAF_ASNS":"1,3,15,15",
                                   "INTF_NAME":"Loopback0",
                                   "SERIAL_NUMBER":"",
                                   "FABRIC_NAME":"",
                                   "POLICY_ID":"",
                                   "ENABLE_TRM":"false",
                                   "ENABLE_BGP_AUTH":"false",
                                   "BFD_ENABLE":"false",
                                   "BFD_BGP_ENABLE":"false"},
                        "entityName":"SWITCH",
                        "entityType":"SWITCH",
                        "source":"",
                        "priority":500,
                        "description":"Spine Overlay",
                        "templateName":"ebgp_overlay_spine_all_neighbor",
                        "serialNumber":"0000001,0000002"}
