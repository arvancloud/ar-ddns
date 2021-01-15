import socket
import sys

import requests
from requests.exceptions import RequestException

from arvancloud_ddns.arvancloud_dns_api import ArvanCloudDNSAPI
from arvancloud_ddns.constant import PUBLIC_IP_FINDER_SERVICES
from arvancloud_ddns.exceptions import RecordNotFound

def find_api_address():
    ip_address = ''
    for finder in PUBLIC_IP_FINDER_SERVICES:
        try:
            result = requests.get(finder)
        except requests.RequestException:
            continue
        if result.status_code == 200:
            try:
                socket.inet_aton(result.text)
                ip_address = result.text
                break
            except socket.error:
                try:
                    socket.inet_aton(result.json().get('ip'))
                    ip_address = result.json()['ip']
                    break
                except socket.error:
                    continue
    if ip_address == '':
        print('None of public ip finder is working. Please try later')
        sys.exit(1)

    return ip_address


def sync_public_ip(ar: ArvanCloudDNSAPI, dns_type='a', cloud = False):
        """
        Sync dns from my public ip address.
        It will not do update if ip address in dns record is already same as
        current public ip address.
        :param ar: ArvanCloudDNSAPI instance
        :param dns_type:
        :param cloud
        :return:
        """
        ip_address = find_api_address()
        try:
            record = ar.get_record(dns_type)
        except RecordNotFound:
            ar.create_record(dns_type, ar.domain,
                               ip_address, cloud=cloud)
            print('Successfully created new record with IP address {new_ip}'
                  .format(new_ip=ip_address))
        else:
            if record['value'][0]['ip'] != ip_address:
                old_ip = record['value'][0]['ip']
                ar.update_record(dns_type, ip=ip_address, cloud=cloud)
                print('Successfully updated IP address from {old_ip} to {new_ip}'
                      .format(old_ip=old_ip, new_ip=ip_address))
            else:
                print('IP address on Arvancloud is same as your current address')
