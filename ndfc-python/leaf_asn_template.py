#!/usr/bin/python
# Author Ahamed Sadayan
# Template for http post leaf ASN policy for BGP fabric
# After import make changes to the relevant field

leaf_asn_policy = {"nvPairs":{"BGP_AS":"4290000121",
                        "FABRIC_NAME":"",
                        "SERIAL_NUMBER":"",
                        "POLICY_ID":""},
                    "entityName":"SWITCH","entityType":"SWITCH","source":"","priority":500,
                    "description":"leaf_asn",
                    "templateName":"leaf_bgp_asn",
                    "serialNumber":"DUMMY1234NA,DUMMY56789F"}
