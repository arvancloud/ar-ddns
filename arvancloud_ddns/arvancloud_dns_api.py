import sys
import urllib

import requests
from requests.exceptions import HTTPError

from arvancloud_ddns.exceptions import RecordNotFound, ZoneNotFound


class ArvanCloudDNSAPI:
    """
    ArvanCloud dns tools class
    """
    api_url = 'https://napi.arvancloud.com/cdn/4.0/domains'
    domain = None
    api_key = None
    records = None

    def __init__(self, api_key: str, domain: str):
        """
        Initialization. It will set the zone information of the domain for operation.
        It will also get dns records of the current zone.
        :param api_key:
        :param domain:
        """
        self.api_key = "Apikey {}".format(api_key)

        domain_segments = domain.split(".")
        # Join the last two segments of the domain name.
        self.domain = domain_segments[-2] + "." + domain_segments[-1]
        self.api_url = self.api_url + '/' + domain + '/dns-records'

        self.headers = {
            'Authorization': self.api_key,
        }

    def setup_records(self):
        """
        Get list of DNS records
        :return:
        """
        try:
            records = self.api(self.api_url, 'get')
        except HTTPError:
            raise ZoneNotFound('Cannot find zone information for the domain {domain}.'
                               .format(domain=self.domain))

        if not records['data']:
            raise ZoneNotFound('Cannot find zone information for the domain {domain}.'
                               .format(domain=self.domain))
        self.records = records['data']

    def api(self, url, method, data=None):
        """
        The requester shortcut to submit a http api to ArvanCloud
        :param url:
        :param method:
        :param data:
        :return:
        """
        method = getattr(requests, method)
        response = method(
            url,
            headers=self.headers,
            json=data,
        )
        content = response.json()
        if response.status_code != 200:
            print(content)
            raise HTTPError(content['message'])
        return content

    def get_record(self, dns_type):
        """
        Get a dns record
        :param dns_type:
        :param name:
        :return:
        """
        try:
            record = [
                record for record in self.records if record['type'] == dns_type]
        except IndexError:
            raise RecordNotFound(
                'Cannot find the specified dns record in domain {domain}'
                .format(domain=self.domain))
        return record[0]

    def create_record(self, dns_type, name, ip, **kwargs):
        """
        Create a dns record
        :param dns_type:
        :param name:
        :param content:
        :param kwargs:
        :return:
        """
        data = {
            'type': dns_type,
            'name': name,
            'value': {
                'ip': ip
            }
        }
        if kwargs.get('ttl') and kwargs['ttl'] != 1:
            data['ttl'] = kwargs['ttl']
        if kwargs.get('cloud') is True:
            data['cloud'] = True
        else:
            data['cloud'] = False
        content = self.request(
            self.api_url,
            'post',
            data=data
        )
        self.dns_records.append(content['data'])
        print('DNS record successfully created')
        return content

    def update_record(self, dns_type, **kwargs):
        """
        Update dns record
        :param dns_type:
        :param name:
        :param content:
        :param kwargs:
        :return:
        """

        """
        type
        name
        value: array
            ip
        ttl
        cloud
        """
        record = self.get_record(dns_type)

        if kwargs.get('ttl') and kwargs['ttl'] != 1:
            record['ttl'] = kwargs['ttl']
        if kwargs.get('cloud') is True:
            record['cloud'] = True
        else:
            record['cloud'] = False
        if kwargs.get('ip'):
            record['value'][0]['ip'] = kwargs['ip']

        if dns_type == 'a':
            self.update_a_record(record)
        else:
            print("other record types not supported yet")
            sys.exit(1)

    def update_a_record(self, record):
        content = self.api(
            self.api_url, '/' + record['id'],
            'put',
            data=record
        )
        print('DNS record successfully updated')
        return content

    def create_or_update_record(self, dns_type, name, content, **kwargs):
        pass

    def delete_record(self, dns_type, name):
        pass
