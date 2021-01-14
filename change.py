import json
import requests
from requests.structures import CaseInsensitiveDict
from time import sleep
from ifaddr import get_adapters

API_KEY = "Apikey XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX"
API_URL_BASE = "https://napi.arvancloud.com/cdn/4.0"

headers = CaseInsensitiveDict()
headers["Authorization"] = API_KEY

SLEEP_TIME = 5

def send_request(
    uri: str,
    method: str = "GET",
    data: dict = {}
):
    if method.casefold() == "put":
        response = requests.put(uri, headers=headers, data=data)
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
        updated_dns_record = dns.copy()
        if dns_type == 'ipv4' and dns['type'] == 'a':
            for ip in dns['value']:
                if ip["ip"] in changes.keys():
                    updated_ip = ip.copy()
                    updated_ip['ip'] = changes[ip['ip']][0]
                    updated_dns_record['value'].remove(ip)
                    updated_dns_record['value'].append(updated_ip)
                    update_dns(updated_dns_record, record['domain'])


def update_dns(dns_record: dict, domain: str):
    API_URL = f"{API_URL_BASE}/domains/{domain}/dns-records/{dns_record['id']}"
    payload = {
        "type": dns_record['type'],
        "name": dns_record['name'],
        "value": dns_record['value'],
        "ttl": dns_record['ttl'],
        "cloud": dns_record['cloud'],
        "upstream_https": dns_record['upstream_https'],
        "ip_filter_mode": dns_record['ip_filter_mode']
    }
    return send_request(API_URL, 'PUT', data=payload)

if __name__ == "__main__":
    # a     => IPv4
    # aaaa  => IPv6
    update_dns_types = 'ipv4'
    update_domain_name = "DOMAIN-NAME"
    current_ips = find_all_ips(update_dns_types)
    while True:
        current_ips, changes = check_ips_changed(current_ips, update_dns_types)
        if changes:
            find_changed_records(changes, find_domain(update_domain_name), update_dns_types)            
        sleep(SLEEP_TIME)

