#!/bin/bash

sudo ip link set dev eth3 up

sudo modprobe br_netfilter
sudo sysctl -p /etc/sysctl.conf
sudo /home/student/firewall_rules.sh

sudo npm install -g forever

IP_ONE=None
IP_TWO=None
IP_THREE=None
IP_FOUR=None
IP_FIVE=None

PORT_ONE=None
PORT_TWO=None
PORT_THREE=None
PORT_FOUR=None
PORT_FIVE=None

sudo rm -f /home/student/$PORT_ONE
sudo rm -f /home/student/$PORT_TWO
sudo rm -f /home/student/$PORT_THREE
sudo rm -f /home/student/$PORT_FOUR
sudo rm -f /home/student/$PORT_FIVE

sudo ip addr add "$IP_ONE"/24 brd + dev eth3
sudo ip addr add "$IP_TWO"/24 brd + dev eth3
sudo ip addr add "$IP_THREE"/24 brd + dev eth3
sudo ip addr add "$IP_FOUR"/24 brd + dev eth3
sudo ip addr add "$IP_FIVE"/24 brd + dev eth3

sudo iptables -t nat -I PREROUTING -s 0.0.0.0/0 -d "$IP_ONE" --protocol tcp --dport 22 -j DNAT --to-destination 10.0.3.1:"$PORT_ONE"
sudo iptables -t nat -I PREROUTING -s 0.0.0.0/0 -d "$IP_TWO" --protocol tcp --dport 22 -j DNAT --to-destination 10.0.3.1:"$PORT_TWO"
sudo iptables -t nat -I PREROUTING -s 0.0.0.0/0 -d "$IP_THREE" --protocol tcp --dport 22 -j DNAT --to-destination 10.0.3.1:"$PORT_THREE"
sudo iptables -t nat -I PREROUTING -s 0.0.0.0/0 -d "$IP_FOUR" --protocol tcp --dport 22 -j DNAT --to-destination 10.0.3.1:"$PORT_FOUR"
sudo iptables -t nat -I PREROUTING -s 0.0.0.0/0 -d "$IP_FIVE" --protocol tcp --dport 22 -j DNAT --to-destination 10.0.3.1:"$PORT_FIVE"

mkdir -p /home/student/mitm_logs

mkdir -p /home/student/mitm_logs/hospital_low_low
mkdir -p /home/student/mitm_logs/hospital_low_high
mkdir -p /home/student/mitm_logs/hospital_high_low
mkdir -p /home/student/mitm_logs/hospital_high_high

mkdir -p /home/student/mitm_logs/bank_low_low
mkdir -p /home/student/mitm_logs/bank_low_high
mkdir -p /home/student/mitm_logs/bank_high_low
mkdir -p /home/student/mitm_logs/bank_high_high

mkdir -p /home/student/mitm_logs/restaurant_low_low
mkdir -p /home/student/mitm_logs/restaurant_low_high
mkdir -p /home/student/mitm_logs/restaurant_high_low
mkdir -p /home/student/mitm_logs/restaurant_high_high

sudo forever stopall

all_containers=$(sudo lxc-ls)

for container in $all_containers; do
    echo "Stopping container: $container"
    sudo lxc-stop -n "$container"

    echo "Destroying container: $container"
    sudo lxc-destroy -n "$container" 
done

mkdir -p /home/student/hunnypot_logs

touch "/home/student/hunnypot_logs/$PORT_ONE.log"
touch "/home/student/hunnypot_logs/$PORT_TWO.log"
touch "/home/student/hunnypot_logs/$PORT_THREE.log"
touch "/home/student/hunnypot_logs/$PORT_FOUR.log"
touch "/home/student/hunnypot_logs/$PORT_FIVE.log"

echo "$(date +"%Y-%m-%d %H:%M:%S"): Running create script" >> "/home/student/hunnypot_logs/$PORT_ONE.log"
echo "$(date +"%Y-%m-%d %H:%M:%S"): Running create script" >> "/home/student/hunnypot_logs/$PORT_TWO.log"
echo "$(date +"%Y-%m-%d %H:%M:%S"): Running create script" >> "/home/student/hunnypot_logs/$PORT_THREE.log"
echo "$(date +"%Y-%m-%d %H:%M:%S"): Running create script" >> "/home/student/hunnypot_logs/$PORT_FOUR.log"
echo "$(date +"%Y-%m-%d %H:%M:%S"): Running create script" >> "/home/student/hunnypot_logs/$PORT_FIVE.log"

sudo /home/student/create.sh $IP_ONE $PORT_ONE&
sudo /home/student/create.sh $IP_TWO $PORT_TWO&
sudo /home/student/create.sh $IP_THREE $PORT_THREE&
sudo /home/student/create.sh $IP_FOUR $PORT_FOUR&
sudo /home/student/create.sh $IP_FIVE $PORT_FIVE& 

sudo apt-get install zip -y
