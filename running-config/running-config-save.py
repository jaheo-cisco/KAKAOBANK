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

from cli import cli

LOCAL_FILE ="bootflash:/running-config.txt"


def get_run_config() -> str:
    """

    """
    print("Querying running-config...")
    running_config = cli("show running-config")
    print("Done. Collected running-config.")

    return running_config

def get_time() -> str:
    """

    """
    current_time = cli("show clock").split()[0]
    valid_time_string = current_time.replace(':', '_')
    print("파일이 생성된 시간은 다음과 같습니다.")
    print(valid_time_string)
    print("현재 시간을 장비에서 추출 완료하였습니다.")

    return valid_time_string

def write_file(running_config: str, valid_time_string: str) -> None:
    """
    Write running-config to file
    """
    LOCAL_FILE = f"/bootflash/running-config_{valid_time_string}.txt"
    print(f"다음 파일에 Running-config를 저장합니다.: {LOCAL_FILE}")
    
    with open(LOCAL_FILE, "w") as file:
        file.write(running_config)
    print("완료되었습니다. Running-config가 저장되었습니다.")
    print("파일의 이름은 다음과 같습니다.")
    print(LOCAL_FILE)

def run():
    print("Running-config 저장 파이썬 스크립트를 시작합니다.")

    current_running_config = get_run_config()
    valid_time_string = get_time()

    write_file(current_running_config,valid_time_string)
    print("스크립트를 종료합니다.")


if __name__ == "__main__":
    run()


    
