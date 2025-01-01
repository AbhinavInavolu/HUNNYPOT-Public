import zipfile
import json


def extract_zip(zip_file, extract_path):
    with zipfile.ZipFile(zip_file, 'r') as zip_ref:
        zip_ref.extractall(extract_path)

def dump_json(data, file_path):
    with open(file_path, 'w') as json_file:
        json.dump(data, json_file, indent=4, default=str)

def dump_text(data, file_path):
    with open(file_path, "w") as file:
        for line in data:
            file.write(f"{line}\n")
