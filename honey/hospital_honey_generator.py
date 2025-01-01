from faker import Faker
import random
import json

fake = Faker()

# Function to generate a random medical history from predefined conditions
def generate_medical_history():
    conditions = [
        "Hypertension", "Diabetes", "Asthma", "COPD", "Heart Disease", 
        "Kidney Stones", "Arthritis", "Migraine", "Depression", 
        "Anxiety", "Cancer", "None"
    ]
    
    # Randomly select 1 to 3 conditions from the list
    return random.sample(conditions, k=random.randint(1, 3))

# Function to generate billing information for the patient
def generate_billing_info():
    return {
        "billing_ID": fake.uuid4(),  # Unique billing ID
        "total_amount": round(random.uniform(100, 10000), 2),  # Total bill amount between $100 and $10,000
        "outstanding_balance": round(random.uniform(0, 5000), 2)  # Outstanding balance, up to $5,000
    }

# Function to generate insurance information for the patient
def generate_insurance_info():
    return {
        "insurance_company": fake.company(),  # Random company name
        "policy_number": fake.uuid4()  # Unique policy number
    }

# Function to generate a complete patient record
def generate_patient_record():
    return {
        "name": fake.name(),  # Patient's name
        "age": random.randint(1, 100),  # Random age between 1 and 100
        "sex": random.choice(["Male", "Female"]),  # Randomly assign sex
        "medical_history": generate_medical_history(),  # Medical history from the predefined list
        "billing_information": generate_billing_info(),  # Billing details
        "address": fake.address(),  # Patient's address
        "insurance_information": generate_insurance_info()  # Insurance details
    }

# Function to write multiple patient records to a JSON file
def write_records_to_file(filename, num_records):
    # Generate a list of patient records
    patient_records = [generate_patient_record() for _ in range(num_records)]

    # Write the records to a file in JSON format
    with open("./" + filename, 'w') as file:
        json.dump(patient_records, file, indent=4)

    print(f"Records saved to {filename}")

# Main function to generate and save patient records
if __name__ == "__main__":
    print("Generating records...")
    write_records_to_file("hospital_honey.json", 10)  # Generate 10 records
    print("Records generated and saved.")
