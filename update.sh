#!/bin/bash

#################
# Configuration #
#################

API_KEY=""
DOMAIN=""
RECORD_ID="" # Resolve with command: curl -X GET -H "Authorization: $API_KEY" "https://napi.arvancloud.com/cdn/4.0/domains/$DOMAIN/dns-records"
IP_STORE_FILE="lastip.txt"

##########
# Script #
##########

# Check if IP changed
IP=$(curl -s ifconfig.me)
LAST_IP=$(cat $IP_STORE_FILE)

if [ -f "$IP_STORE_FILE" ] && [ $LAST_IP == $IP ]; then
    echo "[$(date)] IP not changed"
    exit
fi

# Update record in ArvanCloud

RESULT=$(curl -s -o /dev/null -w '%{http_code}' -X PUT -H "Authorization: $API_KEY" "https://napi.arvancloud.com/cdn/4.0/domains/$DOMAIN/dns-records/$RECORD_ID" -d "name=%40&type=A&value=%5B%7B+%22ip%22%3A+%22$IP%22%7D%5D")

# Check update result

if [ $RESULT -eq 200 ]; then
    # Save last updated ip
    echo $IP > $IP_STORE_FILE
    
    echo "[$(date)] Record successfully updated, current IP: $IP"
else
    echo "[$(date)] Error in updating record, current IP: $IP"
fi
