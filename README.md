# ar-ddns
ArvanCloud Dynamic DNS Tool

# Brief
Some Times the origin servers don't have the static IP and their IP may change after a while. With this tool the user can update DNS record in ArvanCloud DNS service automatically.

## Input
- User API Token available in ArvanCloud panel which can be found from https://npanel.arvancloud.com/profile/api-keys 
- User Subdomain.

## Capabalities
* Set DNS Record 
* Update DNS Record

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
For example your domain is www.example.com. After adding the Input variables, the script will look for your current DNS records and find the type "a" for "www" record. Then the script checks for your server's IP address. If there is a match for your current address and server's address no action will be taken. otherwise Your "www" record will be changed to your server's IP address. Set first argument as API Key abd second argument as your subdomain. and run the following command:
```
./ddns.sh "Apikey 54654654654" "www.example.com"
```
If you want to change "@" record just add root domain as follow:
```
./ddns.sh "Apikey 54654654654" "example.com"
```

