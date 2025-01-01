from hashlib import sha256
from faker import Faker
import random
import json  

# Initialize Faker instance for generating fake data
fake = Faker()

# Function to generate hashed password using SHA-256
def generate_password_hash(password: str) -> str:
    return sha256(password.encode()).hexdigest()

# Function to generate a single user profile with account and transaction data
def generate_profile() -> dict:    
    # Profile details with fake personal, account, and transaction data
    profile = {
        "username": fake.user_name(),
        "password_hash": generate_password_hash(fake.password()),
        "customer_account_data": {
            "name": fake.name(),
            "address": fake.address(),
            "phone_number": f"{fake.phone_number()}",
            "email_address": f"{fake.user_name()}@example.com", 
            "account_balance": round(random.uniform(100, 100000), 2),  # Random balance between 100 and 100k
            "loan_information": {
                "loan_amount": round(random.uniform(1000, 500000), 2),  # Loan amount between 1k and 500k
                "loan_type": random.choice(["personal", "mortgage", "auto", "business"])  # Random loan type
            }
        },
        "transactions": generate_transactions()  # List of fake transactions
    }
    return profile

# Function to generate a list of random transactions
def generate_transactions() -> list:
    num_transactions = random.randint(10, 100)
    transactions = []

    for _ in range(num_transactions):
        transactions.append({
            "recipient_account": fake.iban(),  # Random recipient IBAN
            "sender_account": fake.iban(),     # Random sender IBAN
            "transaction_amount": round(random.uniform(10, 5000), 2),  # Random amount between 10 and 5000
            "timestamp": fake.date_time_this_year().isoformat()  # Timestamp from the current year
        })

    return transactions

# Function to create multiple user profiles
def create_profiles(num_profiles=10) -> list:
    profiles = []

    for _ in range(num_profiles):
        profiles.append(generate_profile())  # Append generated profile to the list

    return profiles

# Function to save profiles to a JSON file
def write_profiles_to_file(filename, num_profiles):
    profiles = create_profiles(num_profiles)

    with open("./" + filename, 'w') as file:
        json.dump(profiles, file, indent=4)  # Save profiles as formatted JSON

    print(f"Profiles saved to {filename}")

# Main function to generate and save profiles
if __name__ == "__main__":
    print("Generating profiles...")
    write_profiles_to_file("bank_honey.json", 10)
    print("Profiles generated and saved.")
