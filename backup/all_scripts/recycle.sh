#!/bin/bash
# Usage: ./recycle.sh <EXTERNAL IP> <MITM PORT>

# if [ "$#" -ne 2 ]; then
#   echo "Usage: $0 <EXTERNAL IP> <MITM PORT>"
# fi

EXTERN_IP=$1
MITM_PORT=$2
CONTAINER=$3

# Destroy the old container
echo "$(date +"%Y-%m-%d %H:%M:%S"): Running destroy script" >> "/home/student/hunnypot_logs/$MITM_PORT.log"
sudo /home/student/destroy.sh $EXTERN_IP $MITM_PORT $CONTAINER #> /dev/null 2>&1

# Create a new container
echo "$(date +"%Y-%m-%d %H:%M:%S"): Running create script" >> "/home/student/hunnypot_logs/$MITM_PORT.log"
sudo /home/student/create.sh $EXTERN_IP $MITM_PORT& #> /dev/null 2>&1 &
