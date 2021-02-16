#!/bin/bash


### get arguments
while getopts d:a:i: option
do
case "${option}"
in
a) TOKEN=${OPTARG};;
d) domain_name=${OPTARG};;
i) IP=${OPTARG};;
esac
done

if [ "$TOKEN" == "" ] || [ "$domain_name" == "" ]; then
	echo "API key and domain name are required"
	exit 1
fi


root_domain=$(echo $domain_name | awk -F\. '{print $(NF-1) FS $NF}' )

###check if its a root domain ro subdomain
if [ "$(echo $domain_name | awk -F"." '{print $3}')" == "" ] ; then
	subdomain="@"
else 
	subdomain=$(echo $domain_name | awk -F"." '{print $1}')
fi

### get current IP From Arvancloud DNS
data=$(curl -s -L -X GET \
   "https://napi.arvancloud.com/cdn/4.0/domains/$root_domain/dns-records" \
   -H "Content-Type: application/json" \
   -H "Accept: application/json" \
   -H "Authorization: ${TOKEN}")
current_IP=$(echo $data | jq '.data[] | select(.type=="a") |  select(.name=="'$subdomain'") ' | jq '.value[].ip' 2> /dev/null  | sed 's/^"\(.*\)".*/\1/') 
domain_id=$(echo $data |  jq '.data[] | select(.type=="a")   |  select(.name=="'$subdomain'") ' | jq '.id' 2> /dev/null | sed 's/^"\(.*\)".*/\1/' )

### get system's current IP
if [ "$IP" == "" ]; then
	response=$(curl -s -o /dev/null -w ''%{http_code}'' https://ipinfo.io/ip);
	if [ "${response}" != "200" ]; then
		response=$(curl -s https://wtfismyip.com/text)
		IP=$response
	else
		response=$(curl -s  https://ipinfo.io/ip)
		IP=$response
	fi
fi

### set System's current IP into Arvancloud DNS
if  [ "${current_IP}" == "${response}" ] ; then
	echo "No action Needed"
else
    if [ "${domain_id}" != "" ]; then
	    PutNewIP=$(curl -s -L -X PUT "https://napi.arvancloud.com/cdn/4.0/domains/$root_domain/dns-records/$domain_id" \
       -H "Content-Type: application/json" \
       -H "Accept: application/json" \
       -H "Authorization: ${TOKEN}" \
       -d "{ \"name\": \"$subdomain\", \"type\": \"a\", \"value\": [{\"ip\": \"$IP\"}]}")
   else
       PutNewIP=$(curl -s -L -X POST "https://napi.arvancloud.com/cdn/4.0/domains/$root_domain/dns-records/" \
       -H "Content-Type: application/json" \
       -H "Accept: application/json" \
       -H "Authorization: ${TOKEN}" \
       -d "{ \"name\": \"$subdomain\", \"type\": \"a\", \"value\": [{\"ip\": \"$IP\"}]}")
   fi
echo $PutNewIP
fi
