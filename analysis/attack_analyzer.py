import requests
from analysis.map import create_map
from utils.file_utils import dump_json, dump_text
from constants import *

from collections import defaultdict
from operator import itemgetter
import pandas as pd
import re


def parse_attacks_data(attacks_data):
    command_frequency = defaultdict(int) 
    download_commands_data = set()

    attacks_per_ip = {ip: 0 for ip in PORT_TO_IP.values()}
    attacks_per_config = {config: 0 for config in CONFIGS}
    attacks_per_client_id = defaultdict(int)
    attacks_per_source_ip = defaultdict(int)
    unique_attacks = defaultdict(set)

    download_commands = ["wget", "curl", "scp", "rsync", "ftp", "tftp", "sftp"]

    for _, attack_data in attacks_data.items():
        destination_ip = attack_data.get("Destination_IP")
        config = attack_data.get("Configuration")
        client_id = attack_data.get("Client_ID")
        source_ip = attack_data.get("Source_IP")
        commands = attack_data.get("Commands")

        unique_attacks[config].add(source_ip)

        attacks_per_ip[destination_ip] += 1
        attacks_per_config[config] += 1
        attacks_per_client_id[client_id] += 1
        attacks_per_source_ip[source_ip] += 1
        for command in commands:
            command_frequency[command] += 1

            split_command = command.split(" ")
            if len(split_command) > 1 and (split_command[0] in download_commands or split_command[1] in download_commands):
                download_commands_data.add(command)

    command_frequency = dict(sorted(command_frequency.items(), key=lambda item: item[1], reverse=True))

    download_commands_data, urls = prioritize_ip_lines(download_commands_data)

    dump_json(command_frequency, COMMAND_FREQUENCY_JSON)
    dump_text(download_commands_data, DOWNLOAD_COMMANDS_TXT)
    dump_text(urls, URLS_TXT)

    with pd.ExcelWriter(ATTACK_REPORT_XLSX) as writer:
        count_attacks_per_IP(attacks_per_ip, writer)
        count_unique_ips_per_config(unique_attacks, writer)
        count_attacks_per_config(attacks_per_config, writer)
        count_client_ids(attacks_per_client_id, writer)
        count_attacks_per_unique_ip(attacks_per_source_ip, writer)

    create_map(attacks_per_source_ip)

def prioritize_ip_lines(command_list):
    ip_pattern = r'\b\d+\.\d+\.\d+\.\d+\b' 
    url_pattern = re.compile(r'(https?://[^\s]+)')
    
    ip_lines = []
    non_ip_lines = []
    urls = set()
    
    for line in command_list:
        if re.search(ip_pattern, line):
            ip_lines.append(line)  
        else:
            non_ip_lines.append(line)  

        urls_found = url_pattern.findall(line)
        for url in urls_found:
            urls.add(url)
    
    return ip_lines + non_ip_lines, urls

def count_attacks_per_IP(attacks_per_ip, writer):
    total = sum(attacks_per_ip.values())
    table = [[ip, count] for ip, count in attacks_per_ip.items()]
    table.append(["Total", total])

    df = pd.DataFrame(table, columns=["IP Address", "Attacks"])
    df.to_excel(writer, sheet_name="Attacks per IP", index=False)

def count_unique_ips_per_config(unique_attacks, writer):
    table = [[config, len(ips)] for config, ips in unique_attacks.items()]
    df = pd.DataFrame(table, columns=["Config", "Unique IPs"])
    df.to_excel(writer, sheet_name="Unique IPs per Config", index=False)

def count_attacks_per_config(attacks_per_config, writer):
    table = [[config, count] for config, count in attacks_per_config.items()]
    df = pd.DataFrame(table, columns=["Config", "Attacks"])
    df.to_excel(writer, sheet_name="Attacks per Config", index=False)

def count_client_ids(attacks_per_client_id, writer):
    sorted_client_ids = sorted(attacks_per_client_id.items(), key=itemgetter(1), reverse=True)
    df = pd.DataFrame(sorted_client_ids, columns=["Client ID", "Attacks"])
    df.to_excel(writer, sheet_name="Attacks per Client ID", index=False)

def count_attacks_per_unique_ip(attacks_per_source_ip, writer):
    sorted_attacks_per_source_ip = sorted(attacks_per_source_ip.items(), key=itemgetter(1), reverse=True)

    top_1 = len(sorted_attacks_per_source_ip) // 100

    df = pd.DataFrame(sorted_attacks_per_source_ip[:top_1], columns=["Source IP", "Attacks"])
    df.to_excel(writer, sheet_name="Attacks per Source IP", index=False)

    orgs = defaultdict(int)

    for ip, freq in sorted_attacks_per_source_ip[:top_1*10]:
        response = requests.get(f"https://ipinfo.io/{ip}/json")
        if response.status_code == 200: 
            orgs[response.json().get("org")] += freq   
        else:
            print("Error fetching data for IP:", ip)      
