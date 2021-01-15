# arvancloud-ddns
ArvanCloud Dynamic DNS Tool

# Brief
Some Times the origin servers don't have the static IP and their IP may change after a while. With this tool the user can update DNS record in ArvanCloud DNS service automatically.

## Options
- -a User API Token available in ArvanCloud panel which can be found from https://npanel.arvancloud.com/profile/api-keys 
- -d User Subdomain
- -i IP address (optional)

## Capabalities
* Set DNS Record 
* Update DNS Record

# Bash Script

## Requirements
The jq package is required.

### Centos
```
 yum install jq -y
```
### Debian
```
apt install jq -y
```
## Examples
For example your domain is www.example.com. After adding the Input variables, the script will look for your current DNS records and find the type "a" for "www" record. By default the script checks for your server's IP address unless you set -i argument. If there is a match for your current address in your Avan panel and server's address no action will be taken. otherwise Your "www" record will be changed to your server's IP address. The following command changes "www" record for "example.com" domain to "8.8.8.8".
```
./ddns.sh -a "Apikey 54654654654" -d "www.example.com" -i "8.8.8.8"
```
If you want to change "@" record just add root domain as follow:
```
./ddns.sh -a "Apikey 54654654654" -d "example.com"
```

# Python Script

## Installation
    pip install arvancloud-ddns

## Examples
    arvancloud-ddns --api-key YOUR-ARVANCLOUD-API-KEY --domain YOUR-DOMAIN

