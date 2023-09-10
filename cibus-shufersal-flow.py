import requests
from coupons_generator import optimized_algo, greedy_algo
from constants import CouponsKind

# Create a session
session = requests.Session()

# Define the login information
username = "<YOUR USERNAME HERE>"
password = "<YOUR PASSWORD HERE>"
company = "מיקרוסופט"

# Define the additional header
headers = {
    "Application-Id": "E5D5FEF5-A05E-4C64-AEBA-BA0CECA0E402"
}

mysodexo_url = "https://api.mysodexo.co.il/api/main.py"

def login(session):
    login_payload = {
        "type": "prx_login",
        "user": username,
        "password": password,
        "company": company,
        "remember": True
    }
    response = session.post(mysodexo_url, json=login_payload, headers=headers)
    if response.status_code != 200:
        print("Login failed. Status code:", response.status_code)
        exit()

    # Check if the login was successful
    login_response = response.json()
    if login_response.get("code") == 726:
        print("Login failed:", login_response.get("msg"))
        exit()
    
    return response

def get_budget(session):
    get_budget_payload = {
        "mode": "raw",
        "type": "prx_get_budgets"
    }
    response = session.post(mysodexo_url, json=get_budget_payload, headers=headers)

    return response

def add_to_cart(session, dish_price):
    add_to_cart_payload = {
        "type": "prx_add_prod_to_cart",
        "order_type": 2,
        "dish_list": {
            "category_id": 4723015,
            "dish_id": 4807364,  # You can replace this with a variable if needed
            "dish_price": dish_price,
            "co_owner_id": -1,
            "extra_list": []
        }
    }
    response = session.post(mysodexo_url, json=add_to_cart_payload, headers=headers)
    if response.status_code != 200:
        print("Adding item to cart failed. Status code:", response.status_code)
        exit()

    return response

def get_cart_info(session):
    get_cart_payload = {
        "type": "prx_get_cart"
    }
    response = session.post(mysodexo_url, json=get_cart_payload, headers=headers)
    if response.status_code != 200:
        print("Getting cart information failed. Status code:", response.status_code)
        exit()

    # Print the cart information
    cart_data = response.json()
    print(cart_data)

    return response

# Step 1: Perform login and get the token cookie
login_response = login(session)
# Step 2: Get the budget
budget = get_budget(session)
coupons_prices = optimized_algo(budget, CouponsKind.SHUFERSAL)
for price in coupons_prices:
    # Step 3: Add item to the cart (using default dish_id)
    add_to_cart(session, price)
    # Step 4: Get cart information
    get_cart_info(session)
    # Step 5: Apply order
    # TODO: Apply_order (==Pay)
    


