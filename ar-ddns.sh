#!/bin/bash

# Usage:
# ar-ddns.sh -k Arvan API-KEY \
#            -d example.com   \
#            -r 18


CHECKIPSITE="http://ipv4.icanhazip.com"


# get cli parameters
while getopts k:d:r:n: opts; do
  case ${opts} in
    k) ARKEY=${OPTARG} ;;
    d) DOMAIN=${OPTARG} ;;
    r) RECORD_ID=${OPTARG} ;;
    n) RECORD_NAME=${OPTARG} ;;
  esac
done

# If required settings are missing just exit
if [ "$ARKEY" = "" ]; then
  echo "Missing arvan Api Key"
  exit 2
fi

if [ "$DOMAIN" = "" ]; then
  echo "Missing Domain"
  exit 2
fi

if [ "$RECORD_ID" = "" ]; then
  echo "Missing RECORD ID"
  exit 2
fi
if [ "$RECORD_NAME" = "" ]; then
  echo "Missing RECORD Name"
  exit 2
fi

# Get Current & Old IP
IP=`curl -s ${CHECKIPSITE}`
IP_FILE="ar-last-ip.txt"
if [ -f $IP_FILE ]; then
  OLD_IP=`cat $IP_FILE`
else
  OLD_IP=""
fi

# If IP not changed
if [ "$IP" = "$OLD_IP" ]; then
  echo "IP not changed"
  exit 0
fi

# Script

RESPONSE=$(curl -s -o /dev/null -w -X PUT "https://napi.arvancloud.com/cdn/4.0/domains/$DOMAIN/dns-records/$RECORD_ID" \
  -H "Authorization: $ARKEY" \
  -H "Content-Type: application/json" \
  --data "{\"type\":\"a\",\"name\":\"$RECORD_NAME\",\"value\":\"[{\"ip\": \"$IP\"}]'\"}")


if [ $RESPONSE -eq 200 ]; then
  echo "Record Updated succesfuly!"
  echo $IP > $IP_FILE
  exit
else
  echo 'Failed :('
  exit 1
fi
