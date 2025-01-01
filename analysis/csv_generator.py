from utils.constants import ALL_CSV, UNIQUE_CSV

import csv


def generate_csv_reports(attacks_data):
    all_output = []
    unique_output = []
    source_ips = set()

    for _, attack_info in attacks_data.items():
        config = attack_info.get("Configuration", "")
        org = "".join(config.split("_")[0])
        ram = "".join(config.split("_")[1])
        cpu = "".join(config.split("_")[2])

        duration_seconds = attack_info.get("Duration", "")
        num_commands = len(attack_info.get("Commands", ""))
        source = attack_info.get("Source_IP", "")

        data_point = {
            'Config': config,
            'Organization': org,
            'RAM': ram,
            'CPU': cpu,
            'Source IP': source,
            'Duration_Seconds': duration_seconds,
            'Num_Commands': num_commands
        }

        if duration_seconds != 300: 
            all_output.append(data_point)

            if source not in source_ips:
                unique_output.append(data_point)
    
        source_ips.add(source)

    with open(ALL_CSV, 'w', newline='') as all_file, \
            open(UNIQUE_CSV, 'w', newline='') as unique_file:

        fieldnames = all_output[0].keys()

        all_writer = csv.DictWriter(all_file, fieldnames=fieldnames)
        unique_writer = csv.DictWriter(unique_file, fieldnames=fieldnames)

        all_writer.writeheader()
        unique_writer.writeheader()

        all_writer.writerows(all_output)
        unique_writer.writerows(unique_output)
