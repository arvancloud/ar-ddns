import click

from arvancloud_ddns.arvancloud_dns_api import ArvanCloudDNSAPI
from arvancloud_ddns.utils import sync_public_ip


@click.command()
@click.option('--domain', required=True)
@click.option('--api-key', required=True)
@click.option('--cloud', is_flag=True,
              help='by activating this option, the usage will be calculated based on four variables: Input traffic, Output traffic, HTTP/HTTPS requests, and the number of Cache Purge requests.')
@click.option('--dry-run', is_flag=True,
              help='Use the --dry-run option to run arvancloud-ddns without changing your dns.')
def cli(domain, api_key, dry_run=False, cloud=False):
    ar = ArvanCloudDNSAPI(api_key, domain)
    ar.setup_records()
    sync_public_ip(ar, cloud=cloud)
