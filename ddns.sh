#!/bin/bash

TOKEN="Apikey "
domain_name="example.com"

root_domain=$(echo $domain_name | awk -F\. '{print $(NF-1) FS $NF}' )

if [ "$(echo $domain_name | awk -F"." '{print $3}')" == "" ] ; then
	subdomain="@"
else 
	subdomain=$(echo $domain_name | awk -F"." '{print $1}')
fi

data=$(curl -s -L -X GET \
   "https://napi.arvancloud.com/cdn/4.0/domains/$root_domain/dns-records" \
   -H "Content-Type: application/json" \
   -H "Accept: application/json" \
   -H "Authorization: ${TOKEN}")


current_IP=$(echo $data | jq '.data[] | select(.type=="a") |  select(.name=="'$subdomain'") ' | jq '.value[].ip' 2> /dev/null)
domain_id=$(echo $data |  jq '.data[] | select(.type=="a")   |  select(.name=="'$subdomain'") ' | jq '.id' 2> /dev/null | sed 's/^"\(.*\)".*/\1/' )

response=$(curl -s -o /dev/null -w ''%{http_code}'' https://wtfismyip.com/text);
if [ "${response}" == "200" ]; then
	response=$(curl -s https://wtfismyip.com/text)
else
	response=$(curl -s  https://ipinfo.io/ip)
fi

if  [ ${current_IP} == "${response}" ] ; then
	echo "No action Needed"
else
	PutNewIP=$(curl -s -L -X PUT "https://napi.arvancloud.com/cdn/4.0/domains/$root_domain/dns-records/$domain_id" \
   -H "Content-Type: application/json" \
   -H "Accept: application/json" \
   -H "Authorization: ${TOKEN}" \
   -d "{"name": "$subdomain", "type": "a", "value": "[{"ip": "$response"}]"}")
echo $PutNewIP
fi
