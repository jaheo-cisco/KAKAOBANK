#!/usr/bin/python
# Author Ahamed Sadayan
# Template for http post leaf ASN policy for BGP fabric
# After import make changes to the relevant field


leaf_overlay_policy = {"nvPairs":{"SPINE_IP_LIST":"0.0.0.0,1.1.1.1",
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
                       "description":"overlay_leaf_to_spine",
                       "templateName":"ebgp_overlay_leaf_all_neighbor",
                       "serialNumber":"000000,000001,000002,00003,00004"}


