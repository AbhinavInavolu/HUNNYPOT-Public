#!/bin/bash

# Usage: ./create.sh <EXTERNAL IP> <MITM PORT>
# if [ "$#" -ne 2 ]; then
#   echo "Usage: $0 <EXTERNAL IP> <MITM PORT>"
# fi

EXTERN_IP=$1
MITM_PORT=$2

# Randomly select configuration
NAME=$((1 + "$RANDOM" % 3))
RAM=$((1 + "$RANDOM" % 2))
CPU=$((1 + "$RANDOM" % 2))

RAM_AMT=$((RAM * 2147483648))
CPU_AMT=$((CPU * 512))

FILENAME=""

# Create name variable based on random nums
if [ "$NAME" == 1 ]; then
    NAME=bank
    FILENAME="bank_honey.json"
elif [ "$NAME" == 2 ]; then
    NAME=hospital
    FILENAME="hospital_honey.json"
else
    NAME=restaurant
    FILENAME="restaurant_honey.json"
fi

# Create RAM variable based on random nums
if [ "$RAM" == 1 ]; then
    RAM=_low_
else
    RAM=_high_
fi

# Create CPU variable based on random nums
if [ "$CPU" == 1 ]; then
    CPU=low
else
    CPU=high
fi

EPOCH_TIME=$(date +%s)
NEW_FOLDER="${NAME}${RAM}${CPU}"
NEW_CONTAINER="${NEW_FOLDER}_${MITM_PORT}_${EPOCH_TIME}"

echo "$(date +"%Y-%m-%d %H:%M:%S"): Creating container" >> "/home/student/hunnypot_logs/$MITM_PORT.log"
sudo lxc-create -n "$NEW_CONTAINER" -t download -- -d ubuntu -r focal -a amd64
sudo lxc-start -n "$NEW_CONTAINER"
echo "$(date +"%Y-%m-%d %H:%M:%S"): Created Container" >> "/home/student/hunnypot_logs/$MITM_PORT.log"

echo "$(date +"%Y-%m-%d %H:%M:%S"): Waiting for container to start" >> "/home/student/hunnypot_logs/$MITM_PORT.log"
while ! sudo lxc-info -n "$NEW_CONTAINER" | grep -q "RUNNING"; do
    sleep 1
done

# Set RAM and CPU Limit
sudo lxc-cgroup -n "$NEW_CONTAINER" memory.limit_in_bytes "$RAM_AMT"
sudo lxc-cgroup -n "$NEW_CONTAINER" cpu.shares "$CPU_AMT"

# Fetch the internal IP and store it for routing
while true; do
    IP=$(sudo lxc-info -n "$NEW_CONTAINER" -iH 2>/dev/null)

    if [ -n "$IP" ]; then
        break
    fi

    sleep 1
done
echo "$(date +"%Y-%m-%d %H:%M:%S"): Container started" >> "/home/student/hunnypot_logs/$MITM_PORT.log"

# Install binaries on the honeypot
echo "$(date +"%Y-%m-%d %H:%M:%S"): Installing Binaries" >> "/home/student/hunnypot_logs/$MITM_PORT.log"
sudo lxc-attach -n "$NEW_CONTAINER" -- bash -c "sudo apt-get update"
sudo lxc-attach -n "$NEW_CONTAINER" -- bash -c "sudo apt-get install openssh-server -y"
sudo lxc-attach -n "$NEW_CONTAINER" -- bash -c "sudo systemctl enable ssh --now"

while true; do
    FLAG=$(sudo lxc-attach -n "$NEW_CONTAINER" -- bash -c 'command -v sshd &> /dev/null && systemctl is-active ssh')

    if [ -n "$FLAG" ]; then
        break
    fi
    
    sleep 1
done
echo "$(date +"%Y-%m-%d %H:%M:%S"): Openssh is running" >> "/home/student/hunnypot_logs/$MITM_PORT.log"

# Add the honey to the new container
sudo cp /home/student/honey/$FILENAME /var/lib/lxc/$NEW_CONTAINER/rootfs/home

# Insert MITM rule
sudo iptables -t nat -A PREROUTING -s 0.0.0.0/0 -d $EXTERN_IP -j DNAT --to-destination $IP
sudo iptables -t nat -I POSTROUTING -s $IP -d 0.0.0.0/0 -j SNAT --to-source $EXTERN_IP

# Allow routing of localnet traffic
sudo sysctl -w net.ipv4.conf.all.route_localnet=1

# Set up MITM server
echo "$(date +"%Y-%m-%d %H:%M:%S"): Starting MITM" >> "/home/student/hunnypot_logs/$MITM_PORT.log"
sudo forever -l /home/student/mitm_logs/"$NEW_FOLDER"/"$NEW_CONTAINER".log start -a /home/student/MITM/mitm.js -n "$NEW_CONTAINER" -i "$IP" -p "$MITM_PORT" --mitm-ip 10.0.3.1 --auto-access --auto-access-fixed 1 --debug

echo "$(date +"%Y-%m-%d %H:%M:%S"): MITM is running" >> "/home/student/hunnypot_logs/$MITM_PORT.log"

echo "$(date +"%Y-%m-%d %H:%M:%S"): Running tail script" >> "/home/student/hunnypot_logs/$MITM_PORT.log"
sudo /home/student/tail.sh $EXTERN_IP $MITM_PORT $NEW_CONTAINER&

