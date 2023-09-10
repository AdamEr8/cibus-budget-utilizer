import requests

# Create a session
session = requests.Session()

# Define the login information
username = "<YOUR USERNAME HERE>"
password = "<YOUR PASSWORD HERE>"

# Define the additional header
headers = {
    "Application-Id": "E5D5FEF5-A05E-4C64-AEBA-BA0CECA0E402"
}

# Step 1: Perform login and get the token cookie
login_url = "https://api.mysodexo.co.il/api/main.py"
login_payload = {
    "type": "prx_login",
    "user": username,
    "password": password,
    "company": "",
    "remember": True
}

response = session.post(login_url, json=login_payload, headers=headers)
if response.status_code != 200:
    print("Login failed. Status code:", response.status_code)
    exit()

# Check if the login was successful
login_response = response.json()
if login_response.get("code") == 726:
    print("Login failed:", login_response.get("msg"))
    exit()

# Step 2: Add item to the cart (using default dish_id)
add_to_cart_url = "https://api.mysodexo.co.il/api/main.py"
add_to_cart_payload = {
    "type": "prx_add_prod_to_cart",
    "order_type": 2,
    "dish_list": {
        "category_id": 4723015,
        "dish_id": 4807364,  # You can replace this with a variable if needed
        "dish_price": 100,
        "co_owner_id": -1,
        "extra_list": []
    }
}

response = session.post(add_to_cart_url, json=add_to_cart_payload, headers=headers)
if response.status_code != 200:
    print("Adding item to cart failed. Status code:", response.status_code)
    exit()

# Step 3: Get cart information
get_cart_url = "https://api.mysodexo.co.il/api/main.py"
get_cart_payload = {
    "type": "prx_get_cart"
}

response = session.post(get_cart_url, json=get_cart_payload, headers=headers)
if response.status_code != 200:
    print("Getting cart information failed. Status code:", response.status_code)
    exit()

# Print the cart information
cart_data = response.json()

print(cart_data)
