#!/usr/bin/env python3

import simplejson as json
import argparse
import os
import requests
import sys
import time
import urllib3
import subprocess

secret_key = "4htwt6MCV9oGTOpaTS0"
url = "https://beta.iwe.cloud/backend/servers/query/by-tags"
headers = {"secret-key": secret_key, "tags": "all"}

ssh_dir = os.path.expanduser('~/.ssh/iwe')

ssh_config_template = "Host {}\n\tuser root\n\tIdentityFile {}\n\tHostName {}\n"

def get_server_list():
    try:
        request = requests.get(url, headers=headers)
    except (urllib3.exceptions.NewConnectionError, requests.exceptions.ConnectionError):
        print ('Connection error!')
        return None
    if request.status_code == 200:
        return request.json()
    else:
        return None


def main():
    servers = get_server_list()

    for server in servers:
        id_rsa_path = ssh_dir + "/id_rsa_{}".format(server)
        with open(id_rsa_path, 'w+') as ssh_priv:
            ssh_priv.write(servers[server]['sshkey_priv'])

        print(ssh_config_template.format(server,
                ssh_dir + "/id_rsa_{}".format(server),
                servers[server]['vpn_ipv4']))

if __name__ == "__main__":
    main()
