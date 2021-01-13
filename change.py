import json
import requests
from requests.structures import CaseInsensitiveDict
from time import sleep
from ifaddr import get_adapters

API_KEY = "Apikey 4baa5745-ad26-42e1-b29c-74975f7f9bb5"
API_URL_BASE = "https://napi.arvancloud.com/cdn/4.0"

headers = CaseInsensitiveDict()
headers["Authorization"] = API_KEY

SLEEP_TIME = 5

def send_request(
    uri: str,
    method: str = "GET",
):
    if method.casefold() == "PUT":
        response = requests.get(uri, headers=headers)
    else:
        response = requests.get(uri, headers=headers)
        
    if response.status_code == 200 :
        json_data = json.loads(response.content.decode("utf-8"))['data']
    else:
        return False
    
    return json_data

def find_domain(domain: str):
    API_URL = f"{API_URL_BASE}/domains/{domain}"
    return send_request(API_URL, 'GET')

def find_dns(domain: str):
    API_URL = f"{API_URL_BASE}/domains/{domain}/dns-records"
    return send_request(API_URL, 'GET')

def find_current_public_ip(dns_type: str = 'ipv4'):
    if dns_type == 'ipv4':
        ip = requests.get('https://api.ipify.org').text.strip()
    else:
        ip = requests.get('https://api64.ipify.org').text.strip()
    return ip

def find_current_interfaces_ips(adapters, dns_type: str = 'ipv4'):
    interfaces = {}
    for item in adapters:
        for ip in item.ips:
            if ip.is_IPv4 and dns_type == 'ipv4':
                interfaces[item.name] = ip.ip
            elif ip.is_IPv6 and dns_type == 'ipv6':
                interfaces[item.name] = ip.ip
    return interfaces

def find_all_ips(dns_type: str = 'ipv4'):
    adapters = get_adapters()
    ips = find_current_interfaces_ips(adapters, dns_type)
    ips['public'] = find_current_public_ip(dns_type)
    return ips

def check_ips_changed(ips: dict, dns_type: str = 'ipv4'):
    adapters = get_adapters()
    current_ips = find_all_ips(dns_type)
    changes = {}
    for item in ips:
        if ips[item] != current_ips[item]:
            try:
                changes[ips[item]] = [current_ips[item]]
            except:
                pass
    return current_ips, changes

def find_changed_records(changes: dict, record: dict, dns_type: str = 'ipv4'):
    for dns in find_dns(record['domain']):
        if dns_type == 'ipv4' and dns['type'] == 'a':
            for ip in dns['value']:
                if ip["ip"] in changes.keys():
                    update_dns(dns, ip["ip"], changes[ip['ip']])

def update_dns(dns, ip, change):
    print(dns)
    print(ip)
    print(change)

if __name__ == "__main__":
    update_dns_types = 'ipv4'
    update_domain_name = "test33.com"
    current_ips = find_all_ips(update_dns_types)
    while True:
        current_ips, changes = check_ips_changed(current_ips, update_dns_types)
        if changes:
            find_changed_records(changes, find_domain(update_domain_name), update_dns_types)            
        sleep(SLEEP_TIME)

