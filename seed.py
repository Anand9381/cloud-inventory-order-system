import requests
import json
import random
import time

BASE_URL = "http://localhost:5000/api"

def seed_users():
    suffix = random.randint(1000, 9999)
    users = [
        {"username": f"alice_{suffix}", "email": f"alice_{suffix}@example.com"},
        {"username": f"bob_{suffix}", "email": f"bob_{suffix}@example.com"},
        {"username": f"charlie_{suffix}", "email": f"charlie_{suffix}@example.com"},
        {"username": f"dave_{suffix}", "email": f"dave_{suffix}@example.com"}
    ]
    created_ids = []
    print(f"Seeding Users (Suffix: {suffix})...")
    for user in users:
        try:
            res = requests.post(f"{BASE_URL}/users", json=user)
            if res.status_code == 201:
                uid = res.json()['id']
                created_ids.append(uid)
                print(f"  Created user: {user['username']} (ID: {uid})")
            else:
                print(f"  Error creating {user['username']}: {res.text}")
        except Exception as e:
            print(f"  Failed: {e}")
    return created_ids

def seed_products():
    suffix = random.randint(1000, 9999)
    products = [
        {"name": "Laptop", "price": 999.99, "sku": f"TECH-001-{suffix}", "stock": 50, "description": "High performance laptop"},
        {"name": "Smartphone", "price": 499.50, "sku": f"TECH-002-{suffix}", "stock": 100, "description": "Latest 5G smartphone"},
        {"name": "Headphones", "price": 79.99, "sku": f"AUDIO-001-{suffix}", "stock": 200, "description": "Noise cancelling headphones"},
        {"name": "Monitor", "price": 150.00, "sku": f"TECH-003-{suffix}", "stock": 30, "description": "24-inch 1080p monitor"},
        {"name": "Keyboard", "price": 45.00, "sku": f"ACC-001-{suffix}", "stock": 75, "description": "Mechanical keyboard"}
    ]
    created_ids = []
    print("\nSeeding Products...")
    for p in products:
        try:
            res = requests.post(f"{BASE_URL}/products", json=p)
            if res.status_code == 201:
                pid = res.json()['id']
                created_ids.append(pid)
                print(f"  Created product: {p['name']} (ID: {pid})")
            else:
                print(f"  Error creating {p['name']}: {res.text}")
        except Exception as e:
            print(f"  Failed: {e}")
    return created_ids

def seed_orders(user_ids, product_ids):
    if not user_ids or not product_ids:
        print("Skipping orders (missing users or products)")
        return

    print("\nSeeding Orders...")
    for _ in range(5): # Create 5 random orders
        uid = random.choice(user_ids)
        items = []
        # Random items per order
        for _ in range(random.randint(1, 3)):
            pid = random.choice(product_ids)
            qty = random.randint(1, 2)
            items.append({"product_id": pid, "quantity": qty})
        
        order_data = {"user_id": uid, "items": items}
        
        try:
            res = requests.post(f"{BASE_URL}/orders", json=order_data)
            if res.status_code == 201:
                oid = res.json()['id']
                print(f"  Created Order #{oid} for User {uid}")
            else:
                print(f"  Error creating order: {res.text}")
        except Exception as e:
            print(f"  Failed: {e}")

if __name__ == "__main__":
    print("Waiting for server to start...")
    time.sleep(2) # Give it a moment if running right after start
    
    u_ids = seed_users()
    p_ids = seed_products()
    seed_orders(u_ids, p_ids)
    
    print("\nSeeding Complete! Check MySQL Workbench and MongoDB Compass.")
