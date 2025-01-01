HOSTNAME = None
USERNAME = None
PASSWORD = None
PORT = None

IP_ONE = None
IP_TWO = None
IP_THREE = None
IP_FOUR = None
IP_FIVE = None

PORT_ONE = None
PORT_TWO = None
PORT_THREE = None
PORT_FOUR = None
PORT_FIVE = None

PORT_TO_IP = {
    PORT_ONE: IP_ONE, 
    PORT_TWO: IP_TWO,
    PORT_THREE: IP_THREE,
    PORT_FOUR: IP_FOUR,
    PORT_FIVE: IP_FIVE
}

LOGS_GLOB = './assets/mitm_logs/*/*'
GEO_IP_DATABASE = './assets/GeoLite2-City_20241108/GeoLite2-City.mmdb'
WORLD_CITIES_CSV = './assets/cities/worldcities.csv'

PARSED_OUTPUT_DIR = './analysis/parsed/'

PARSED_JSON = f'{PARSED_OUTPUT_DIR}/parsed_attacks.json'
ALL_CSV = f'{PARSED_OUTPUT_DIR}/all.csv'
UNIQUE_CSV = f'{PARSED_OUTPUT_DIR}/unique.csv'
COMMAND_FREQUENCY_JSON = f'{PARSED_OUTPUT_DIR}/command_frequency.json'
ATTACK_REPORT_XLSX = f'{PARSED_OUTPUT_DIR}/attack_report.xlsx'
DOWNLOAD_COMMANDS_TXT = f'{PARSED_OUTPUT_DIR}/download_commands.txt'
URLS_TXT = f'{PARSED_OUTPUT_DIR}/urls.txt'
WORLD_MAP = f'{PARSED_OUTPUT_DIR}/world_map.html'

CONFIGS = ["bank_high_high", "bank_high_low", "bank_low_high", "bank_low_low", 
           "hospital_high_high", "hospital_high_low", "hospital_low_high", "hospital_low_low", 
           "restaurant_high_high", "restaurant_high_low", "restaurant_low_high", "restaurant_low_low"]

CORRELATION_THRESHOLD = 0.5
