from nornir import InitNornir
from nornir_napalm.plugins.tasks import napalm_get, napalm_cli, napalm_configure
from nornir.core.filter import F
from nornir.core.task import Task
import json


# Initialize Nornir with a configuration file
nr = InitNornir(config_file="config.yml")
result = nr.run(
    task=napalm_get,
    getters=["facts"],
)

print("Fetching Facts from each device..")
result = nr.run(
    task=napalm_get,
    getters=["facts"],
)

# 결과를 파싱하고 JSON 파일로 저장
data = {}
for host in result:
    facts = result[host].result["facts"]
    hostname = facts["hostname"]
    serial_number = facts["serial_number"]
    os_version = facts["os_version"]
    data[host] = {
        "hostname": hostname,
        "serial_number": serial_number,
        "os_version": os_version,
    }
# Print the data
for host, info in data.items():
    print(f"Hostname: {info['hostname']}")
    print(f"Serial Number: {info['serial_number']}")
    print(f"OS Version: {info['os_version']}")
    print("--------------------")
# JSON 파일로 저장
with open('result.json', 'w') as f:
    json.dump(data, f, indent=4)

print("Data saved to result.json")

    # Gather interfaces facts
result = nr.run(
    task=napalm_get,
    getters=["facts", "interfaces"],
)
# Parse the output and shutdown interfaces without description

# Open the file in write mode

with open('shutdown_commands.txt', 'w') as file:
    print("Parse the output and write shutdown commands for interfaces without description")
    for host in result:
        for interface, details in result[host].result["interfaces"].items():
            description = details.get("description")
            if interface != 'mgmt0' and (not description or description.strip() == ''):
                print("interface shutting down...")
                print(f"Interface {interface} description: {description}")
                # Write the shutdown command to the file
                file.write(f"interface {interface}\n")
                file.write("shutdown\n")
        print("interface shutdown Complete")
        print("--------------------")

# Now you can use the 'shutdown_commands.txt' file to shutdown the interfaces
conf_result=nr.run(task=napalm_configure, filename="shutdown_commands.txt")

cli_results=nr.run(task=napalm_cli, commands=["show int b"])
