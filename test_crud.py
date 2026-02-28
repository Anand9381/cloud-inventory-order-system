import requests
import sys

BASE_URL = 'http://localhost:5000/api'

def test_user_crud():
    print("\n--- Testing User CRUD ---")
    # 1. Create User
    username = "crud_test_user"
    email = "crud_test@example.com"
    
    # Clean up first if exists (optional, but good for idempotency if running multiple times)
    # But since we don't have ID, we just try create and handle error or use unique suffix
    import random
    suffix = random.randint(1000, 9999)
    username = f"user_{suffix}"
    email = f"user_{suffix}@example.com"

    print(f"Creating user {username}...")
    resp = requests.post(f"{BASE_URL}/users", json={'username': username, 'email': email})
    if resp.status_code != 201:
        print(f"Failed to create user: {resp.text}")
        return
    user = resp.json()
    user_id = user['id']
    print(f"Created User: {user}")

    # 2. Read User
    print(f"Reading user {user_id}...")
    resp = requests.get(f"{BASE_URL}/users/{user_id}")
    if resp.status_code != 200:
        print(f"Failed to read user: {resp.text}")
        return
    print(f"Read User: {resp.json()}")

    # 3. Update User
    print(f"Updating user {user_id}...")
    new_username = f"updated_{username}"
    resp = requests.put(f"{BASE_URL}/users/{user_id}", json={'username': new_username})
    if resp.status_code != 200:
        print(f"Failed to update user: {resp.text}")
        return
    print(f"Updated User: {resp.json()}")

    # 4. Delete User
    print(f"Deleting user {user_id}...")
    resp = requests.delete(f"{BASE_URL}/users/{user_id}")
    if resp.status_code != 200:
        print(f"Failed to delete user: {resp.text}")
        return
    print("User deleted successfully.")

    # Verify deletion
    resp = requests.get(f"{BASE_URL}/users/{user_id}")
    if resp.status_code == 404:
        print("Verification: User not found (correct).")
    else:
        print(f"Verification Failed: User still exists or other error: {resp.status_code}")

def test_product_crud():
    print("\n--- Testing Product CRUD ---")
    import random
    suffix = random.randint(1000, 9999)
    name = f"Product_{suffix}"
    sku = f"SKU_{suffix}"
    
    # 1. Create Product
    print(f"Creating product {name}...")
    data = {
        'name': name,
        'description': "Test Description",
        'price': 100.0,
        'sku': sku,
        'stock': 50
    }
    resp = requests.post(f"{BASE_URL}/products", json=data)
    if resp.status_code != 201:
        print(f"Failed to create product: {resp.text}")
        return
    product = resp.json()
    product_id = product['id']
    print(f"Created Product: {product}")

    # 2. Read Product
    print(f"Reading product {product_id}...")
    resp = requests.get(f"{BASE_URL}/products/{product_id}")
    if resp.status_code != 200:
        print(f"Failed to read product: {resp.text}")
        return
    print(f"Read Product: {resp.json()}")

    # 3. Update Product
    print(f"Updating product {product_id}...")
    resp = requests.put(f"{BASE_URL}/products/{product_id}", json={'price': 150.0, 'stock': 20})
    if resp.status_code != 200:
        print(f"Failed to update product: {resp.text}")
        return
    print(f"Updated Product: {resp.json()}")

    # 4. Delete Product
    print(f"Deleting product {product_id}...")
    resp = requests.delete(f"{BASE_URL}/products/{product_id}")
    if resp.status_code != 200:
        print(f"Failed to delete product: {resp.text}")
        return
    print("Product deleted successfully.")

def test_order_crud():
    print("\n--- Testing Order CRUD ---")
    # Need a user and a product first
    import random
    suffix = random.randint(1000, 9999)
    
    # Setup User
    user_resp = requests.post(f"{BASE_URL}/users", json={'username': f"order_user_{suffix}", 'email': f"order_{suffix}@test.com"})
    user_id = user_resp.json()['id']
    
    # Setup Product
    prod_resp = requests.post(f"{BASE_URL}/products", json={'name': f"Order_Prod_{suffix}", 'price': 50.0, 'sku': f"OSKU_{suffix}", 'stock': 100})
    prod_id = prod_resp.json()['id']

    # 1. Create Order
    print("Creating order...")
    order_data = {
        'user_id': user_id,
        'items': [{'product_id': prod_id, 'quantity': 2}]
    }
    resp = requests.post(f"{BASE_URL}/orders", json=order_data)
    if resp.status_code != 201:
        print(f"Failed to create order: {resp.text}")
        return
    order = resp.json()
    order_id = order['id']
    print(f"Created Order: {order}")

    # 2. Update Order Status
    print(f"Updating order {order_id} status to Completed...")
    resp = requests.put(f"{BASE_URL}/orders/{order_id}", json={'status': 'Completed'})
    if resp.status_code != 200:
        print(f"Failed to update order: {resp.text}")
        return
    print(f"Updated Order: {resp.json()}")

    # 3. Delete Order
    print(f"Deleting order {order_id}...")
    resp = requests.delete(f"{BASE_URL}/orders/{order_id}")
    if resp.status_code != 200:
        print(f"Failed to delete order: {resp.text}")
        return
    print("Order deleted successfully.")


if __name__ == "__main__":
    try:
        test_user_crud()
        test_product_crud()
        test_order_crud()
        print("\nAll CRUD tests completed successfully!")
    except Exception as e:
        print(f"An error occurred: {e}")
