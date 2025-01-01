from faker import Faker
import hashlib
import random
import json

# Initialize Faker
fake = Faker()

# Sample restaurant items
restaurant_items = [
    "Cheeseburger",
    "Margherita Pizza",
    "Caesar Salad",
    "Spaghetti Carbonara",
    "Grilled Salmon",
    "Chicken Tacos",
    "Vegetable Stir Fry",
    "Chocolate Cake",
    "Lemonade",
    "Margarita",
    "Pasta Primavera",
    "Beef Tacos",
    "BBQ Ribs",
    "Fish and Chips",
    "Fried Rice",
]

def generate_password_hash(password):
    return hashlib.sha256(password.encode()).hexdigest()

def generate_fake_honey_data(num_entries):
    honey_data = []
    
    for _ in range(num_entries):
        username = fake.user_name()
        password = fake.password()
        password_hash = generate_password_hash(password)

        # Generate fake data
        name = fake.name()
        
        # Generate fake address
        address = fake.address()

        # Generate a fake phone number
        phone_number = fake.phone_number() 

        # Generate fake email adderss
        email_address = f"fake_{username}@example.com" 

        # Generate prior purchases
        num_purchases = random.randint(1, 5)  # Random number of prior purchases
        prior_purchases = random.sample(restaurant_items, num_purchases)  # Randomly sample items

        customer_account = {
            "username": username,
            "password_hash": password_hash,
            "name": name,
            "address": address,
            "phone_number": phone_number,
            "email_address": email_address,
            "age": random.randint(18, 70),
            "prior_purchases": prior_purchases  # Use realistic restaurant items
        }
        
        honey_data.append(customer_account)

    return honey_data

def save_to_json(data, filename='restaurant_honey.json'):
    with open("./" + filename, 'w') as json_file:
        json.dump(data, json_file, indent=4)

if __name__ == "__main__":
    num_entries = 10  # Number of fake entries you want to generate
    fake_honey_data = generate_fake_honey_data(num_entries)
    save_to_json(fake_honey_data)

    print(f"Generated {num_entries} fake entries and saved to 'restaurant_honey.json'.")
    