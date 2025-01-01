from utils.constants import *
from utils.ip_utils import is_private_ip
from utils.file_utils import dump_json

from datetime import datetime
import glob


def parse_file(log_file_path, attack_id, attacks_data):
    with open(log_file_path, 'r') as file:
        lines = file.readlines()
        
        # Initialize variables
        config = None
        source_ip = None
        destination_ip = None
        client_id = None
        start_time = None
        end_time = None
        last_command_time = None 
        keystrokes_count = 0
        commands = []
        noninteractive_mode = False
        attacker_username = None 
        attacker_password = None 
        
        # Parse lines for relevant data
        for line in lines:
            # Extract Config Name
            if "containerName: '" in line:
                config = "_".join(line.partition("containerName: '")[2].split("_")[:3])
                
            # Extract Source IP and Start Time
            if "Attacker connected:" in line and not start_time:
                tokens = line.split("Attacker connected: ")[1].split(" |")
                client_id = str(tokens[1].split(": ")[1][:-1])
                source_ip = tokens[0]
                start_time = datetime.strptime(line.split(" - ")[0], r"%Y-%m-%d %H:%M:%S.%f")
            
            # Extract Destination IP
            # Count Attacks per Destination IP
            elif "SSH man-in-the-middle server for" in line:
                destination_port = line.split("listening on ")[1].split(":")[1].strip()
                destination_ip = PORT_TO_IP.get(destination_port)
            
            # Extract End Time
            elif "Attacker closed connection" in line or "Attacker closed the connection" in line:
                end_time = datetime.strptime(line.split(" - ")[0], r"%Y-%m-%d %H:%M:%S.%f")
            
            # Count Keystrokes
            elif "[Debug] [SHELL] Attacker Keystroke:" in line:
                keystrokes_count += 1
            
            # Parse Commands
            if "[Debug] [SHELL] line from reader:" in line or "[EXEC] Noninteractive mode attacker command:" in line:
                if "[EXEC] Noninteractive mode attacker command:" in line:
                    noninteractive_mode = True
                    full_command = line.split("Noninteractive mode attacker command: ")[1].strip()
                else:
                    full_command = line.split("line from reader: ")[1].strip()
                
                parse_command(full_command, commands)
                last_command_time = datetime.strptime(line.split(" - ")[0], r"%Y-%m-%d %H:%M:%S.%f")

            # Extract attacker username and password
            elif "[Debug] [Auto Access] Adding the following credentials:" in line:
                attacker_username, _, attacker_password = line.split("'")[1].partition(':')
            
        duration = get_duration(source_ip, start_time, last_command_time, end_time, commands)
        if not duration or attacker_username == "LIBRSYSISVC":
            return attack_id
        
        noninteractive_mode = noninteractive_mode and len(commands) != 0

        # Add parsed data to attacks_data dictionary
        attacks_data[f"Attack-ID {attack_id}"] = {
            "Configuration": config,
            "Source_IP": source_ip,
            "Destination_IP": destination_ip,
            "Client_ID": client_id,
            "Attacker_Username": attacker_username,
            "Attacker_Password": attacker_password,
            "Start_Time": start_time,
            "End_Time": end_time,
            "Duration": duration,
            "Keystrokes_Count": keystrokes_count,
            "Commands": commands, 
            "Noninteractive_Mode": noninteractive_mode,
        }
    
    return attack_id + 1    

def parse_command(full_command, commands):
    for command in full_command.split(";"):
        if command:
            commands.append(command.strip())

def get_duration(source_ip, start_time, last_command_time, end_time, commands):
    # Filter out unattacked logs and test attacks
    if source_ip and not is_private_ip(source_ip): 
        if len(commands) != 0:
            return (last_command_time - start_time).total_seconds()
        else:
            if end_time:
                return (end_time - start_time).total_seconds()
            else:
                return 300
    else:
        return 0

def parse_logs():
    attack_id = 1
    attacks_data = {}

    for log_file_path in glob.glob(LOGS_GLOB):
        attack_id = parse_file(log_file_path, attack_id, attacks_data)

    dump_json(attacks_data, PARSED_JSON)
    
    return attacks_data
