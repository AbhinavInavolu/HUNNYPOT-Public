#!/bin/bash

EXTERN_IP=$1
MITM_PORT=$2
CONTAINER=$3

OPEN_PATTERN="Attacker connected"
CLOSE_PATTERN="closed connection|closed the connection"

LOG_FOLDER=$(echo "$CONTAINER" | cut -d'_' -f1-3 )
LOG_FILE="/home/student/mitm_logs/$LOG_FOLDER/$CONTAINER.log"
FLAG_FILE="/home/student/$MITM_PORT"

CHECK_INTERVAL=1
IDLE_LIMIT=300
MAX_CONNECTION_TIME=1800

# Wait until attack connects
echo "$(date +"%Y-%m-%d %H:%M:%S"): Waiting for attacker" >> "/home/student/hunnypot_logs/$MITM_PORT.log"
tail -F $LOG_FILE | while read -r LINE; do
    if echo "$LINE" | grep -q "$OPEN_PATTERN"; then
        echo "$LINE" | awk '{print $8}' > $FLAG_FILE
        break
    fi
done

ATTACKER_IP=$(cat $FLAG_FILE)
sudo iptables -I INPUT -d 10.0.3.1 -p tcp --dport "$MITM_PORT" -j DROP
sudo iptables -I INPUT -s "$ATTACKER_IP" -d 10.0.3.1 -p tcp --dport "$MITM_PORT" -j ACCEPT

connection_start=$(echo $(date +%s))
last_active=$connection_start
curr_activity=$(cat "$LOG_FILE" | wc -l)

echo "$(date +"%Y-%m-%d %H:%M:%S"): Attacker connected, monitoring log file" >> "/home/student/hunnypot_logs/$MITM_PORT.log"
while true; do
    if cat "$LOG_FILE" | grep -q -E "$CLOSE_PATTERN"; then
        echo "$(date +"%Y-%m-%d %H:%M:%S"): Attacker exited" >> "/home/student/hunnypot_logs/$MITM_PORT.log"
        break
    fi
    
    prev_activity=$curr_activity
    curr_activity=$(cat "$LOG_FILE" | wc -l)

    if (( curr_activity > prev_activity )); then
        last_active=$(date +%s)
    fi

    current_time=$(date +%s)
    idle_time=$((current_time - last_active))
    connection_time=$((current_time - connection_start))

    if (( idle_time >= IDLE_LIMIT )); then
        echo "$(date +"%Y-%m-%d %H:%M:%S"): Attacker reached idle time" >> "/home/student/hunnypot_logs/$MITM_PORT.log"
        break
    fi

    if (( connection_time >= MAX_CONNECTION_TIME )); then
        echo "$(date +"%Y-%m-%d %H:%M:%S"): Attacker reached max time" >> "/home/student/hunnypot_logs/$MITM_PORT.log"
        break
    fi

    sleep 3
done

sudo iptables -D INPUT -d 10.0.3.1 -p tcp --dport "$MITM_PORT" -j DROP
sudo iptables -D INPUT -s "$ATTACKER_IP" -d 10.0.3.1 -p tcp --dport "$MITM_PORT" -j ACCEPT

echo "$(date +"%Y-%m-%d %H:%M:%S"): Running recycle script" >> "/home/student/hunnypot_logs/$MITM_PORT.log"
sudo /home/student/recycle.sh $EXTERN_IP $MITM_PORT $CONTAINER&