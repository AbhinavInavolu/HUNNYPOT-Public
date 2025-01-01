from utils.install_requirements import install_requirements
from utils.file_utils import extract_zip
from constants import *
from utils.ssh_utils import connect_ssh, zip_backup, download_zips, remove_remote_zips
from analysis.log_parser import parse_logs
from analysis.csv_generator import generate_csv_reports
from analysis.attack_analyzer import parse_attacks_data
from analysis.correlations import find_correlations

import time


def measure_time(task_name, func, *args, **kwargs):
    start = time.time()
    result = func(*args, **kwargs)
    end = time.time()

    print(f"{task_name:<30} completed in {end - start:.2f} seconds.")
    return result

if __name__ == "__main__":
    measure_time("Installing dependencies", install_requirements)

    ssh = measure_time("Connecting to remote server", connect_ssh)
    measure_time("Zipping files", zip_backup, ssh)
    measure_time("Downloading zips", download_zips, ssh)
    measure_time("Removing remote zips", remove_remote_zips, ssh)
    ssh.close()

    measure_time("Extracting logs zip", extract_zip, "backup/mitm_logs.zip", "./assets/")

    attacks_data = measure_time("Parsing logs", parse_logs)
    measure_time("Generating CSV reports", generate_csv_reports, attacks_data)
    measure_time("Analyzing attacks", parse_attacks_data, attacks_data)
    measure_time("Finding correlations", find_correlations, attacks_data)

    print("\nAll tasks completed successfully!")
