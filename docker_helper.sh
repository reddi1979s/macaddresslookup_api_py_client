#!/bin/sh

display_usage() { 
	echo 'This container has to be run using docker run --env MACADDRESSIO_API_KEY=key <image_name> macaddresslookup.py <MAC_ADDRESS> <OPTIONAL_PARAMS>'
	echo 'Example: docker run --env MACADDRESSIO_API_KEY=$MY_API_KEY sekher79/macaddresslookupclient:latest macaddresslookup.py E8-40-40-79-C8-60'
    echo 'See Usage: docker run sekher79/macaddresslookupclient:latest macaddresslookup.py -h'
	}
display_usage