#!/bin/bash

# Usage: ./destroy.sh <OLD CONTAINER NAME> <EXTERNAL IP> <MITM PORT>
# if [ "$#" -ne 2 ]; then
#   echo "Usage: $0 <EXTERNAL IP> <MITM PORT>"
# fi

# Grab command line args
EXTERN_IP=$1
MITM_PORT=$2
OLD_CONTAINER=$3

# Fetch old MITM IP
OLD_CONTAINER_IP=$(sudo lxc-info -n $OLD_CONTAINER -iH)

# Saving data about container (CPU I/O, RAM Usage etc)
OLD_FOLDER=$(echo "$OLD_CONTAINER" | cut -d'_' -f1-3 )
sudo lxc-info -n "$OLD_CONTAINER" | sudo tee -a /home/student/mitm_logs/"$OLD_FOLDER"/"$OLD_CONTAINER".log

# Stop old MITM server
ID=$(sudo forever list 2>/dev/null | grep "$OLD_CONTAINER" | xargs | cut -d' ' -f19)
# ID=$(sudo forever list > /dev/null 2>&1| awk -v port="$MITM_PORT" '$0 ~ port {getline; print $3}')
sudo forever stop $ID
echo $ID >> "/home/student/hunnypot_logs/$MITM_PORT.log"
echo "$(date +"%Y-%m-%d %H:%M:%S"): Killing MITM $OLD_CONTAINER $ID" >> "/home/student/hunnypot_logs/$MITM_PORT.log"


# Remove old NAT rules (one by one)
sudo iptables -t nat -D PREROUTING -s 0.0.0.0/0 -d $EXTERN_IP -j DNAT --to-destination $OLD_CONTAINER_IP
sudo iptables -t nat -D POSTROUTING -s $OLD_CONTAINER_IP -d 0.0.0.0/0 -j SNAT --to-source $EXTERN_IP
echo "$(date +"%Y-%m-%d %H:%M:%S"): Removing NAT Rules" >> "/home/student/hunnypot_logs/$MITM_PORT.log"

# Delete container
sudo lxc-stop -n "$OLD_CONTAINER"
sudo lxc-destroy -n "$OLD_CONTAINER"
echo "$(date +"%Y-%m-%d %H:%M:%S"): Destroyed Container $(sudo lxc-info -n $OLD_CONTAINER -iH)" >> "/home/student/hunnypot_logs/$MITM_PORT.log"
