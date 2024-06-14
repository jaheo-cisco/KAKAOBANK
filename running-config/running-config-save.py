"""
Copyright (c) 2023 Cisco and/or its affiliates.
This software is licensed to you under the terms of the Cisco Sample
Code License, Version 1.1 (the "License"). You may obtain a copy of the
License at
               https://developer.cisco.com/docs/licenses
All use of the material herein must be in accordance with the terms of
the License. All rights not expressly granted by the License are
reserved. Unless required by applicable law or agreed to separately in
writing, software distributed under the License is distributed on an "AS
IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
or implied.
"""

import json
from syslog import LOG_ERR, syslog
from typing import Optional

from cisco.vrf import *
from cli import clid

LOCAL_FILE = "/bootflash/py_route_monitor.json"
VRF = "default"


def get_run_config() -> dict:
    """
    Query route table
    """
    print("Querying running-config...")
    running-config = json.loads(clid(f"show running-config"))
    
    print("Done. Collected running-config.")
    return running-config


def write_route_file(routes: dict) -> None:
    """
    Write route list to file
    """
    print(f"Storing current running-config in file: {LOCAL_FILE}")
    with open(LOCAL_FILE, "w") as file:
        file.write(json.dumps(routes))
    print("Done. running-config file saved.")



#def send_syslog(diff: dict) -> None:
#    """
#    Send alert on any changed routes
#    """
#    print("Sending syslog messages to notify route changes...")
#    for route in diff["removed"]:
#        prefix = list(route.keys())[0]
#        syslog(
#            LOG_ERR,
#            f"ROUTE REMOVED - PREFIX: {prefix}, NEXT HOP: {route[prefix]['nexthop']}, PROTOCOL: {route[prefix]['proto']}",
#        )
#    for route in diff["added"]:
#        prefix = list(route.keys())[0]
#        syslog(
#            LOG_ERR,
#            f"ROUTE ADDED - PREFIX: {prefix}, NEXT HOP: {route[prefix]['nexthop']}, PROTOCOL: {route[prefix]['proto']}",
#        )
#    print("Done. Syslog messages sent.")


def run():
    print("Route monitor script started")
    # Query current routing table
    current_running_config = get_run_config()
    # Open last file & compare diffs
    #previous_prefixes = read_route_file()
    #if previous_prefixes:
        # Compare diff
    #    diff = compare_routes(previous_prefixes, current_prefixes)
        # Send syslog on any changes
        #send_syslog(diff)
    # Write new routes file
    write_route_file(current_running_config)
    print("Running-config save finished")


if __name__ == "__main__":
    run()
