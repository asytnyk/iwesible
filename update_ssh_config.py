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
ssh_config_file = os.path.expanduser('~/.ssh/config')

ssh_config_template = "Host {}\n\tuser root\n\tIdentityFile {}\n\tHostName {}\n\tUserKnownHostsFile
/dev/null\n\tStrictHostKeyChecking no\n"

hosts_file_path = os.path.expanduser('~/dev/iwesible/hosts')

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

    if not servers:
        print("Exiting...")
        sys.exit(-1)

    with open(hosts_file_path, 'w+') as hosts_file, \
    open(ssh_config_file, 'w+') as ssh_conf:
        hosts_file.write("[all]\n")

        for server in servers:
            id_rsa_path = ssh_dir + "/id_rsa_{}".format(server)
            with open(id_rsa_path, 'w+') as ssh_priv:
                ssh_priv.write(servers[server]['sshkey_priv'])
            os.chmod(id_rsa_path, 0o600)

            ssh_conf.write(ssh_config_template.format(server,
                    ssh_dir + "/id_rsa_{}".format(server),
                    servers[server]['vpn_ipv4']))
            hosts_file.write("{}\n".format(server))

    os.chmod(ssh_config_file, 0o600)

if __name__ == "__main__":
    main()
